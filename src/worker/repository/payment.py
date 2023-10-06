import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from shared.database.dto import UserPaymentDTO, UserSubscriptionDTO
from shared.database.models import PayStatus, UserPayment
from shared.database.models.base import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

logger = logging.getLogger(__name__)

__all__ = ["UserPaymentsRepository"]


@dataclass
class UserPaymentsRepository:
    _session: Session

    def get_payments_with_status(self, status: str, delay_minutes):
        target_time = datetime.utcnow() - timedelta(minutes=delay_minutes)
        query = (
            select(UserPayment)
            .where(PayStatus.alias == status)
            .join(UserPayment.pay_status)
            .join(UserPayment.pay_system)
            # .with_for_update(skip_locked=True, of=UserPayment)
            .where(UserPayment.created_at <= target_time)
            .options(contains_eager(UserPayment.pay_status))
            .options(contains_eager(UserPayment.pay_system))
            .limit(1)
        )
        payments = self._session.execute(query).scalars()
        result = [UserPaymentDTO.model_validate(payment) for payment in payments]
        return result

    def set_status(self, payment_id: UUID, status: str) -> bool:
        query = select(UserPayment).where(UserPayment.id == payment_id)
        payment_instance = self._session.execute(query).scalar()

        if not payment_instance:
            logger.error("Payment with ID %s not found", payment_id)
            return False

        status_instance = self._get_instance_by_alias(PayStatus, status)

        payment_instance.pay_status_id = status_instance.id
        logger.info("Updated payment %s status to %s", payment_id, status)
        return True

    def create_blank_payment(self, subscription: UserSubscriptionDTO, status: str = "created") -> UserPaymentDTO:
        status_instance = self._get_instance_by_alias(PayStatus, status)
        payment = UserPayment(
            id=uuid4(),
            pay_system_id=subscription.user_payment.pay_system_id,
            pay_status_id=status_instance.id,
            payment_id=subscription.user_payment.payment_id,
            amount=subscription.tariff.cost,
            purpose=subscription.tariff.info(),
            user_id=subscription.user_id,
            json_sale={},
        )
        self._session.add(payment)
        self._session.flush((payment,))
        return UserPaymentDTO.model_validate(payment)

    def _get_instance_by_alias(self, cls: type[BaseModel], alias: str) -> BaseModel:
        if not hasattr(cls, "alias"):
            raise AttributeError(f"{cls.__name__} have no alias")

        query = select(cls).where(cls.alias == alias)
        try:
            cls_instance = self._session.execute(query).scalar_one()
            return cls_instance
        except NoResultFound:
            logger.error("%s with alias %s not found", cls.__name__, alias)
            raise
        except MultipleResultsFound:
            logger.error("%s with alias %s not unique", cls.__name__, alias)
            raise

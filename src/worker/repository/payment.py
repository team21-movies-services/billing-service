import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from shared.database.models import PayStatus
from shared.database.models.user_payment import UserPayment
from shared.schemas.payment import PaymentSchema
from sqlalchemy import select
from sqlalchemy.orm import Session, contains_eager

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
            .with_for_update(skip_locked=True, of=UserPayment)
            .where(UserPayment.created_at <= target_time)
            .options(contains_eager(UserPayment.pay_status))
            .options(contains_eager(UserPayment.pay_system))
            .limit(10)
        )
        payments = self._session.execute(query).scalars()
        result = [
            PaymentSchema(
                id=payment.id,
                status=payment.pay_status.alias,
                system=payment.pay_system.alias,
            )
            for payment in payments
        ]
        return result

    def set_payment_status(self, payment: PaymentSchema) -> bool:
        query = select(UserPayment).where(UserPayment.id == payment.id)
        payment_instance = self._session.execute(query).scalar()

        if not payment_instance:
            logger.error("Payment with ID %s not found", payment.id)
            return False
        query = select(PayStatus).where(PayStatus.alias == payment.status)
        status_instance = self._session.execute(query).scalar()

        if not status_instance:
            logger.error("Status with alias %s not found", payment.status)
            return False

        payment_instance.pay_status_id = status_instance.id
        logger.info("Updated payment %s status to %s", payment.id, payment.status)
        return True

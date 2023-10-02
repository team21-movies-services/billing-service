import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from shared.database.models import PayStatus, PaySystem
from shared.database.models.user_payment import UserPayment
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from worker.clients.database.pg_client import SQLAlchemyProvider
from worker.schemas.payment import PaymentSchema

logger = logging.getLogger(__name__)


@dataclass
class UserPaymentsRepository:
    _provider: SQLAlchemyProvider

    def get_payments_with_status(self, status: str, delay_minutes):
        target_time = datetime.utcnow() - timedelta(minutes=delay_minutes)
        query = (
            select(UserPayment)
            .join(PayStatus)
            .join(PaySystem)
            .where(PayStatus.alias == status)
            .where(UserPayment.created_at <= target_time)
            .options(joinedload(UserPayment.pay_status))
            .options(joinedload(UserPayment.pay_system))
            .limit(10)
        )
        with self._provider.get_session() as session:
            payments: list[UserPayment] = session.execute(query).scalars()
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
        with self._provider.get_session() as session:
            query = select(UserPayment).where(UserPayment.id == payment.id)
            payment_instance = session.execute(query).scalar()

            if not payment_instance:
                logger.error("Payment with ID %s not found", payment.id)
                return False
            query = select(PayStatus).where(PayStatus.alias == payment.status)
            status_instance = session.execute(query).scalar()

            if not status_instance:
                logger.error("Status with alias %s not found", payment.status)
                return False

            payment_instance.pay_status_id = status_instance.id
            session.commit()
            logger.info("Updated payment %s status to %s", payment.id, payment.status)
            return True

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from shared.database.models import PayStatus, PaySystem
from shared.database.models.user_payment import UserPayment
from sqlalchemy.orm import joinedload
from worker.clients.database.pg_client import SQLAlchemyProvider
from worker.schemas.payment import PaymentSchema

logger = logging.getLogger(__name__)


@dataclass
class UserPaymentsRepository:
    _provider: SQLAlchemyProvider

    def get_payments_with_status(self, status: str):
        current_time = datetime.utcnow() + timedelta(minutes=1)

        with self._provider.get_session() as session:
            payments = (
                session.query(UserPayment)
                .join(PayStatus)
                .join(PaySystem)
                .filter(PayStatus.alias == status)
                .filter(UserPayment.created_at <= current_time)
                .options(joinedload(UserPayment.pay_status), joinedload(UserPayment.pay_system))
                .all()
            )
        for payment in payments:
            result = PaymentSchema(id=payment.id, status=payment.pay_status.alias, system=payment.pay_system.alias)
            logger.debug("Got new payments %s", result)
            yield result

    def set_payment_status(self, payment: PaymentSchema) -> bool:
        with self._provider.get_session() as session:
            payment_instance = session.query(UserPayment).filter_by(id=payment.id).first()

            if not payment_instance:
                logger.error("Payment with ID %s not found", payment.id)
                return False

            status_instance = session.query(PayStatus).filter_by(alias=payment.status).first()

            if not status_instance:
                logger.error("Status with alias %s not found", payment.status)
                return False

            payment_instance.pay_status_id = status_instance.id
            session.commit()
            logger.info("Updated payment %s status to %s", payment.id, payment.status)
            return True

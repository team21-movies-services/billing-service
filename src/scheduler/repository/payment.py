import logging
from datetime import datetime

from scheduler.clients.pg_client import SQLAlchemyProvider
from scheduler.schemas.payment import PaymentSchema
from shared.database.models import PayStatus, PaySystem
from shared.database.models.user_payment import UserPayment
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)


class UserPaymentsRepository:
    def __init__(self, provider: SQLAlchemyProvider):
        self._provider: SQLAlchemyProvider = provider

    def get_payments_with_status(self, status: str):
        current_time = datetime.utcnow()

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

    def set_payment_status(self, payment: PaymentSchema):
        ...

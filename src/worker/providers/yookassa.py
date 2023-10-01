import logging

from worker.core.config import Settings
from worker.providers.base_provider import BasePaymentProvider
from worker.schemas.payment import PaymentSchema
from yookassa import Configuration, Payment
from yookassa.client import NotFoundError

logger = logging.getLogger(__name__)


class YookassaPaymentProvider(BasePaymentProvider):
    def __init__(self, settings: Settings):
        Configuration.configure(settings.yookassa.shop_id, settings.yookassa.api_key)

    def get_payment_status(self, payment: PaymentSchema) -> PaymentSchema | bool:
        """Get info from remote payment provider"""
        logger.debug("Checking updates for payment %s", payment.id)
        try:
            # TODO: оставил код для отладки, чтобы не ходить в юкассу, ближе к финалу удалим
            # updated_payment = PaymentSchema(**payment.model_dump())
            # updated_payment.status = "pending"
            updated_payment = Payment.find_one(str(payment.id))
        except NotFoundError:
            logger.error("Payment with id %s not found", payment.id)
            return False
        if updated_payment.status == payment.status:
            logger.debug("Payment %s have still have status %s", payment.id, payment.status)
            return False
        payment.status = updated_payment.status
        logger.debug("Payment %s changed status to %s", payment.id, payment.status)
        return payment

import logging

from worker.schemas.payment import PaymentSchema

from .base_provider import BasePaymentProvider

logger = logging.getLogger(__name__)


class MockPaymentProvider(BasePaymentProvider):
    def get_payment_status(self, payment: PaymentSchema) -> PaymentSchema | None:
        logger.debug("Mock Provider called")
        payment.status = "mocked"
        return payment

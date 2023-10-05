import logging
from uuid import uuid4

from shared.schemas.payment import (
    PaymentAddSchema,
    PaymentResponseSchema,
    PaymentSchema,
)

from .base_provider import BasePaymentProvider

logger = logging.getLogger(__name__)


class MockPaymentProvider(BasePaymentProvider):
    def get_payment_status(self, payment: PaymentSchema) -> PaymentSchema | None:
        logger.debug("Mock Provider called")
        payment.status = "mocked"
        return payment

    def get_return_url(self):
        logger.debug("Mock Provider return url")

    def create_payment(self, payment_add_schema: PaymentAddSchema) -> PaymentResponseSchema | None:
        logger.debug("Mock Provider create payment")
        return PaymentResponseSchema(id=str(uuid4()), status="mock", redirect_url="localhost")

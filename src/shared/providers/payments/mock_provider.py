import logging
from uuid import uuid4

from shared.database.dto import UserSubscriptionDTO
from shared.schemas.payment import (
    PaymentAddSchema,
    PaymentResponseSchema,
    PaymentSchema,
)
from shared.schemas.status import StatusEnum

from .base_provider import BasePaymentProvider

logger = logging.getLogger(__name__)

status_enum_mapping = {
    "mocked": StatusEnum.mocked,
}


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

    def make_recurrent_payment(self, subscription: UserSubscriptionDTO):
        logger.debug("Mock Provider called")

    def map_status(self, status: str) -> StatusEnum:
        return status_enum_mapping[status]

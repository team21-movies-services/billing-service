import logging

from shared.database.dto import UserPaymentDTO, UserSubscriptionDTO

from .base_provider import BasePaymentProvider

logger = logging.getLogger(__name__)


class MockPaymentProvider(BasePaymentProvider):
    def make_recurrent_payment(self, subscription: UserSubscriptionDTO):
        logger.debug("Mock Provider called")

    def get_payment_status(self, payment: UserPaymentDTO) -> str:
        logger.debug("Mock Provider called")
        payment.status = "mocked"
        return payment

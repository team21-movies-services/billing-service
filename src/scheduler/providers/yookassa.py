import logging

from scheduler.clients.http_client import BaseHTTPClient
from scheduler.providers.base_provider import BasePaymentProvider
from scheduler.schemas.payment import PaymentSchema

logger = logging.getLogger(__name__)


class YookassaProvider(BasePaymentProvider):
    def __init__(self, http_client: BaseHTTPClient):
        self.client = http_client

    def get_payment_status(self, payment: PaymentSchema):
        """Get info from remote payment provider"""
        logger.debug("Checking payment %s", payment.id)
        payment.status = "failed"
        logger.debug("Payment %s, %s", payment.id, payment.status)
        return payment

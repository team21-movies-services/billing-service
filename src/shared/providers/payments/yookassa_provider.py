import logging

from requests.exceptions import ConnectionError
from shared.exceptions.clients import HTTPClientException
from shared.providers.payments.base_provider import BasePaymentProvider
from shared.schemas.payment import (
    PaymentAddSchema,
    PaymentResponseSchema,
    PaymentSchema,
)
from shared.settings import YookassaBaseConfig
from yookassa import Configuration, Payment
from yookassa.client import NotFoundError
from yookassa.domain.response.payment_response import PaymentResponse

logger = logging.getLogger(__name__)


class YookassaPaymentProvider(BasePaymentProvider):
    def __init__(self, yookassa_config: YookassaBaseConfig):
        self.yookassa_config = yookassa_config
        Configuration.configure(self.yookassa_config.shop_id, self.yookassa_config.api_key)

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

    def get_return_url(self) -> str:
        return self.yookassa_config.return_url

    def create_payment(self, payment_add_schema: PaymentAddSchema) -> PaymentResponseSchema | None:
        try:
            payment_response: PaymentResponse = Payment.create(payment_add_schema.model_dump())
        except ConnectionError:
            raise HTTPClientException
        if payment_response:
            return PaymentResponseSchema(
                id=str(payment_response.id),
                status=str(payment_response.status),
                redirect_url=str(payment_response.confirmation.confirmation_url),
            )
        return None

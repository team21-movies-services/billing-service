import logging

from shared.database.dto import UserPaymentDTO, UserSubscriptionDTO
from shared.exceptions import PaymentExternalApiException
from worker.core.config import Settings
from worker.schemas.payment import UserPaymentCreatedSchema
from yookassa import Configuration, Payment
from yookassa.client import BadRequestError, NotFoundError

from .base_provider import BasePaymentProvider

logger = logging.getLogger(__name__)


class YookassaPaymentProvider(BasePaymentProvider):
    def __init__(self, settings: Settings):
        Configuration.configure(settings.yookassa.shop_id, settings.yookassa.api_key)

    def get_payment_status(self, payment: UserPaymentDTO) -> str:
        """Get info from remote payment provider"""
        logger.debug("Checking updates for payment %s", payment.id)
        try:
            updated_payment = Payment.find_one(str(payment.id))
        except NotFoundError as e:
            logger.error("Payment with id %s not found", payment.id)
            raise PaymentExternalApiException from e
        if updated_payment.status == payment.pay_status.alias:
            logger.debug("Payment %s have still have status %s", payment.id, payment.pay_status.alias)
            return updated_payment.status
        payment.pay_status.alias = updated_payment.pay_status.alias
        logger.debug("Payment %s changed status to %s", payment.id, payment.pay_status.alias)
        return updated_payment.status

    def make_recurrent_payment(self, subscription: UserSubscriptionDTO) -> UserPaymentCreatedSchema | bool:
        payment_json = subscription.get_yookassa_payment_json()
        try:
            payment = Payment.create(payment_json)
            return UserPaymentCreatedSchema(
                id=payment.id,
                pay_system_alias=subscription.user_payment.pay_system.alias,
                pay_status_alias=payment.status,
                user_id=subscription.user_id,
                payment_id=payment.payment_method.id,
                amount=payment.amount,
                purpose=subscription.tariff.info(),
            )
        except BadRequestError as e:
            logger.error("Payment method with id %s not found", subscription.user_payment.payment_id)
            logger.error("Error message: %s", e)
            raise PaymentExternalApiException from e

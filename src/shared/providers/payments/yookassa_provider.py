import logging

from requests.exceptions import ConnectionError
from shared.database.dto import UserPaymentDTO, UserSubscriptionDTO
from shared.exceptions import PaymentCancelledException, PaymentExternalApiException
from shared.exceptions.clients import HTTPClientException
from shared.providers.payments.base_provider import BasePaymentProvider
from shared.schemas.payment import (
    ErrorAction,
    PaymentAddSchema,
    PaymentResponseSchema,
    UserPaymentCreatedSchema,
)
from shared.schemas.status import StatusEnum
from shared.settings import YookassaBaseConfig
from yookassa import Configuration, Payment
from yookassa.client import (
    ApiError,
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    ResponseProcessingError,
    TooManyRequestsError,
    UnauthorizedError,
)
from yookassa.domain.models import CancellationDetailsReasonCode
from yookassa.domain.response.payment_response import PaymentResponse

logger = logging.getLogger(__name__)


yookassa_exceptions = (
    BadRequestError,
    NotFoundError,
    TooManyRequestsError,
    UnauthorizedError,
    ResponseProcessingError,
    ForbiddenError,
    ApiError,
)


status_enum_mapping = {
    "canceled": StatusEnum.canceled,
    "succeeded": StatusEnum.succeeded,
    "pending": StatusEnum.pending,
    "failed": StatusEnum.failed,
}


class YookassaPaymentProvider(BasePaymentProvider):
    def __init__(self, yookassa_config: YookassaBaseConfig):
        self.yookassa_config = yookassa_config
        Configuration.configure(self.yookassa_config.shop_id, self.yookassa_config.api_key)

    def get_payment_status(self, payment: UserPaymentDTO) -> str:
        """Get info from remote payment provider"""
        logger.debug("Checking updates for payment %s", payment.id)
        try:
            updated_payment = Payment.find_one(str(payment.payment_id))
        except NotFoundError as e:
            logger.error("Payment with id %s not found", payment.payment_id)
            raise PaymentExternalApiException from e
        if updated_payment.status == payment.pay_status.alias:
            logger.debug("Payment %s have still have status %s", payment.payment_id, payment.pay_status.alias)
            return updated_payment.status
        logger.debug("Payment %s changed status to %s", payment.payment_id, updated_payment.status)
        return updated_payment.status

    def make_recurrent_payment(self, subscription: UserSubscriptionDTO) -> UserPaymentCreatedSchema:
        payment_json = subscription.get_yookassa_payment_json()
        try:
            payment = Payment.create(payment_json)
            if payment.status != "succeeded":
                error_action = self._handle_cancellation(payment)
                raise PaymentCancelledException("Payment was cancelled by external API", error_action=error_action)
            logger.info("Payment request results: %s", payment.json())
        except yookassa_exceptions as e:
            raise PaymentExternalApiException from e

        payment_schema = UserPaymentCreatedSchema(
            id=payment.id,
            system_alias=subscription.user_payment.pay_system.alias,
            status_alias=payment.status,
            user_id=subscription.user_id,
            payment_id=payment.payment_method.id,
            amount=payment.amount.value,
            purpose=subscription.tariff.info(),
        )
        return payment_schema

    @staticmethod
    def _handle_cancellation(payment: PaymentResponse):
        set_inactive_list = [
            CancellationDetailsReasonCode.PERMISSION_REVOKED,
            CancellationDetailsReasonCode.PAYMENT_METHOD_RESTRICTED,
            CancellationDetailsReasonCode.CARD_EXPIRED,
        ]
        if payment.cancellation_details.reason in set_inactive_list:
            return ErrorAction.set_inactive

        return ErrorAction.retry

    def map_status(self, status: str) -> StatusEnum:
        return status_enum_mapping[status]

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

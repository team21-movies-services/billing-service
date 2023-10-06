from abc import ABC, abstractmethod

from shared.database.dto import UserSubscriptionDTO
from shared.schemas.payment import (
    PaymentAddSchema,
    PaymentResponseSchema,
    PaymentSchema,
    UserPaymentCreatedSchema,
)
from shared.schemas.status import StatusEnum


class BasePaymentProvider(ABC):
    @abstractmethod
    def get_payment_status(self, payment: PaymentSchema):
        """Get info from remote payment provider"""
        raise NotImplementedError

    @abstractmethod
    def get_return_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_payment(self, payment_add_schema: PaymentAddSchema) -> PaymentResponseSchema | None:
        """Create payment to remote payment provider"""
        raise NotImplementedError

    @abstractmethod
    def make_recurrent_payment(self, subscription: UserSubscriptionDTO) -> UserPaymentCreatedSchema:
        """Make recurrent payment with saved data"""
        raise NotImplementedError

    @abstractmethod
    def map_status(self, status: str) -> StatusEnum:
        """Return mapped payment status"""
        raise NotImplementedError

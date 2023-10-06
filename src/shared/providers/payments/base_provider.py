from abc import ABC, abstractmethod

from shared.schemas.payment import (
    PaymentAddSchema,
    PaymentResponseSchema,
    PaymentSchema,
)


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

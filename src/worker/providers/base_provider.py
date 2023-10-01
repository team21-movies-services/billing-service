from abc import ABC, abstractmethod

from worker.schemas.payment import PaymentSchema


class BasePaymentProvider(ABC):
    @abstractmethod
    def get_payment_status(self, payment: PaymentSchema):
        """Get info from remote payment provider"""
        raise NotImplementedError

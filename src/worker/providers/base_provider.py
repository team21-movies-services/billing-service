from abc import ABC, abstractmethod

from shared.database.dto import UserPaymentDTO, UserSubscriptionDTO
from worker.schemas import UserPaymentCreatedSchema


class BasePaymentProvider(ABC):
    @abstractmethod
    def get_payment_status(self, payment: UserPaymentDTO) -> str:
        """Get info from remote payment provider"""
        raise NotImplementedError

    @abstractmethod
    def make_recurrent_payment(self, subscription: UserSubscriptionDTO) -> UserPaymentCreatedSchema:
        """Make recurrent payment with saved data"""
        raise NotImplementedError

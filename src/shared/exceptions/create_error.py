from .base import BaseCreateError, ExceptionEnum

__all__ = ["PaymentCreateError", "SubscriptionCreateError"]


class CreateExceptionInfo(ExceptionEnum):
    PAYMENT_CREATE_ERROR = "5001", "Some error to create payment."
    SUBSCRIPTION_CREATE_ERROR = "5002", "Some error to create user subscription."


class PaymentCreateError(BaseCreateError):
    """Payment create error Exception"""

    code: str = CreateExceptionInfo.PAYMENT_CREATE_ERROR.code
    error: str = CreateExceptionInfo.PAYMENT_CREATE_ERROR.error


class SubscriptionCreateError(BaseCreateError):
    """Payment create error Exception"""

    code: str = CreateExceptionInfo.SUBSCRIPTION_CREATE_ERROR.code
    error: str = CreateExceptionInfo.SUBSCRIPTION_CREATE_ERROR.error

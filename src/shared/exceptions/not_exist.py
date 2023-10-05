from .base import BaseDoesNotExist, ExceptionEnum


class NotExistsExceptionInfo(ExceptionEnum):
    OBJECT_NOT_EXIST = "3001", "Object does not exists."
    TARIFF_NOT_EXISTS = "3002", "Tariff does not exists."
    USER_SUBSCRIPTION_NOT_EXISTS = "3003", "User doesn't have active subscription"
    PAY_SYSTEM_NOT_EXISTS = "3004", "Pay system not exists."
    PAY_STATUS_SYSTEM_NOT_EXISTS = "3005", "Pay status not exists."


class CreateExceptionInfo(ExceptionEnum):
    PAYMENT_CREATE_ERROR = "5001", "Some error to create payment."


class ObjectDoesNotExist(BaseDoesNotExist):
    """Object does not exist Exception"""

    code: str = NotExistsExceptionInfo.OBJECT_NOT_EXIST.code
    error: str = NotExistsExceptionInfo.OBJECT_NOT_EXIST.error


class TariffDoesNotExist(BaseDoesNotExist):
    """Tariff does not exist Exception"""

    code: str = NotExistsExceptionInfo.TARIFF_NOT_EXISTS.code
    error: str = NotExistsExceptionInfo.TARIFF_NOT_EXISTS.error


class PayStatusDoesNotExist(BaseDoesNotExist):
    """PayStatus does not exist Exception"""

    code: str = NotExistsExceptionInfo.PAY_STATUS_SYSTEM_NOT_EXISTS.code
    error: str = NotExistsExceptionInfo.PAY_STATUS_SYSTEM_NOT_EXISTS.error


class PaymentCreateError(BaseDoesNotExist):
    """Payment create error Exception"""

    code: str = CreateExceptionInfo.PAYMENT_CREATE_ERROR.code
    error: str = CreateExceptionInfo.PAYMENT_CREATE_ERROR.error


class PaySystemDoesNotExist(BaseDoesNotExist):
    """PaySystem does not exist Exception"""

    code: str = NotExistsExceptionInfo.PAY_SYSTEM_NOT_EXISTS.code
    error: str = NotExistsExceptionInfo.PAY_SYSTEM_NOT_EXISTS.error


class UserCurrentSubscriptionNotExist(BaseDoesNotExist):
    code: str = NotExistsExceptionInfo.USER_SUBSCRIPTION_NOT_EXISTS.code
    error: str = NotExistsExceptionInfo.USER_SUBSCRIPTION_NOT_EXISTS.error

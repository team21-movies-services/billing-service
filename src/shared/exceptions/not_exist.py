from .base import BaseDoesNotExist, ExceptionEnum

__all__ = [
    "TariffDoesNotExist",
    "PayStatusDoesNotExist",
    "PaySystemDoesNotExist",
    "UserCurrentSubscriptionNotExist",
]


class NotExistsExceptionInfo(ExceptionEnum):
    OBJECT_NOT_EXIST = "3001", "Object does not exists."
    TARIFF_NOT_EXISTS = "3002", "Tariff does not exists."
    USER_SUBSCRIPTION_NOT_EXISTS = "3003", "User doesn't have active subscription"
    PAY_SYSTEM_NOT_EXISTS = "3004", "Pay system not exists."
    PAY_STATUS_SYSTEM_NOT_EXISTS = "3005", "Pay status not exists."


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


class PaySystemDoesNotExist(BaseDoesNotExist):
    """PaySystem does not exist Exception"""

    code: str = NotExistsExceptionInfo.PAY_SYSTEM_NOT_EXISTS.code
    error: str = NotExistsExceptionInfo.PAY_SYSTEM_NOT_EXISTS.error


class UserCurrentSubscriptionNotExist(BaseDoesNotExist):
    code: str = NotExistsExceptionInfo.USER_SUBSCRIPTION_NOT_EXISTS.code
    error: str = NotExistsExceptionInfo.USER_SUBSCRIPTION_NOT_EXISTS.error

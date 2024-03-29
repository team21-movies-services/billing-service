import enum


class ExceptionEnum(enum.Enum):
    @property
    def code(self):
        return self.value[0]

    @property
    def error(self):
        return self.value[1]


class BaseExceptionInfo(ExceptionEnum):
    BASE_ERROR = "0000", "Something went wrong ..."
    BASE_NOT_EXISTS_ERROR = "3000", "Not exists"
    BASE_CREATE_ERROR = "5000", "Error create"
    BASE_CLIENT_ERROR = "2000", "Something went wrong ..."


class BaseError(Exception):
    """Base exception"""

    code: str = BaseExceptionInfo.BASE_ERROR.code
    error: str = BaseExceptionInfo.BASE_ERROR.error
    detail: str | None = None

    def __init__(self, detail: str | None = None):
        super().__init__(detail)
        self.detail = detail


class BaseDoesNotExist(BaseError):
    """Base does not exist Exception"""

    code: str = BaseExceptionInfo.BASE_NOT_EXISTS_ERROR.code
    error: str = BaseExceptionInfo.BASE_ERROR.error


class BaseClientException(BaseError):
    """Base Client Exception"""

    code: str = BaseExceptionInfo.BASE_CLIENT_ERROR.code
    error: str = BaseExceptionInfo.BASE_CLIENT_ERROR.error


class BaseCreateError(BaseError):
    """Base Create Exception"""

    code: str = BaseExceptionInfo.BASE_CREATE_ERROR.code
    error: str = BaseExceptionInfo.BASE_CREATE_ERROR.error

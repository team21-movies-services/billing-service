from .base import BaseClientException, ExceptionEnum


class ClientsExceptionInfo(ExceptionEnum):
    HTTP_CLIENT_ERROR = "2001", "Error while sending request"


class HTTPClientException(BaseClientException):
    """HTTP Client Exception"""

    code: str = ClientsExceptionInfo.HTTP_CLIENT_ERROR.code
    error: str = ClientsExceptionInfo.HTTP_CLIENT_ERROR.error

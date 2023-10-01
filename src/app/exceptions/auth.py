from .base import BaseAuthException, ExceptionEnum


class AuthExceptionInfo(ExceptionEnum):
    TOKEN_ERROR = "1001", "Something wrong with auth token."
    TOKEN_ENCODE_ERROR = "1002", "Error while encoding your token."
    TOKEN_DECODE_ERROR = "1003", "Error while decoding your token."
    TOKEN_EXPIRED_ERROR = "1004", "Token has been expired."


class TokenException(BaseAuthException):
    """Base Token Exception"""

    code: str = AuthExceptionInfo.TOKEN_ERROR.code
    error: str = AuthExceptionInfo.TOKEN_ERROR.error


class TokenEncodeException(TokenException):
    """Token Encode Exception"""

    code: str = AuthExceptionInfo.TOKEN_ENCODE_ERROR.code
    error: str = AuthExceptionInfo.TOKEN_ENCODE_ERROR.error


class TokenDecodeException(TokenException):
    """Token Decode Exception"""

    code: str = AuthExceptionInfo.TOKEN_DECODE_ERROR.code
    error: str = AuthExceptionInfo.TOKEN_DECODE_ERROR.error


class TokenExpiredException(BaseAuthException):
    """Token Expired Exception"""

    code: str = AuthExceptionInfo.TOKEN_EXPIRED_ERROR.code
    error: str = AuthExceptionInfo.TOKEN_EXPIRED_ERROR.error

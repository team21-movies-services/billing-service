from .base import AuthException


class TokenException(AuthException):
    """Base Token Exception"""


class TokenEncodeException(TokenException):
    """Token Encode Exception"""


class TokenDecodeException(TokenException):
    """Token Decode Exception"""


class TokenExpiredException(AuthException):
    """Token Expired Exception"""

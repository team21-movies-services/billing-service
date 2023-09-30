from .base import BaseAuthException


class TokenException(BaseAuthException):
    """Base Token Exception"""


class TokenEncodeException(TokenException):
    """Token Encode Exception"""


class TokenDecodeException(TokenException):
    """Token Decode Exception"""


class TokenExpiredException(BaseAuthException):
    """Token Expired Exception"""

__all__ = ['PaymentException', 'PaymentExternalApiException']


class PaymentException(Exception):
    pass


class PaymentExternalApiException(PaymentException):
    pass

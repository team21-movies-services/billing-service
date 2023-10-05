__all__ = ['PaymentException', 'PaymentExternalApiException', 'PaymentCancelledException']


class PaymentException(Exception):
    pass


class PaymentExternalApiException(PaymentException):
    pass


class PaymentCancelledException(PaymentException):
    def __init__(self, message, error_action=None):
        super().__init__(message)
        self.error_action = error_action

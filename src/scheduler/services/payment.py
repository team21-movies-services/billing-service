import logging

from scheduler.providers.base_provider import BasePaymentProvider
from scheduler.repository.payment import UserPaymentsRepository

logger = logging.getLogger(__name__)


class PaymentStatusService:
    def __init__(self, payment_repository: UserPaymentsRepository, payment_provider: BasePaymentProvider):
        self._payment_repository = payment_repository
        self._payment_provider = payment_provider

    def check_payments(self):
        payment_gen = self._payment_repository.get_payments_with_status("succeeded")
        for payment in payment_gen:
            self._payment_repository.set_payment_status(payment)
            self._payment_provider.get_payment_status(payment)
            self._payment_repository.set_payment_status(payment)
        logger.debug("Payments checked, next check in %s minutes(no)", "5")

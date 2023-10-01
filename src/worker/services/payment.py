import logging
from dataclasses import dataclass

from worker.core.config import Settings
from worker.providers.factory import ProviderFactory
from worker.repository.payment import UserPaymentsRepository

logger = logging.getLogger(__name__)


@dataclass
class PaymentStatusService:
    _payment_repository: UserPaymentsRepository
    _provider_factory: ProviderFactory
    _settings: Settings

    def update_pending_payments(self):
        payments = self._payment_repository.get_payments_with_status("pending", 5)
        for payment in payments:
            provider = self._provider_factory.get_payment_provider(payment.system)
            updated_payment = provider.get_payment_status(payment)
            if updated_payment:
                is_updated = self._payment_repository.set_payment_status(payment)
                if is_updated:
                    logger.info("Updated payment with id %s to status %s", updated_payment.id, updated_payment.status)
        logger.info("Payments checked, next check in %s minute(s)", self._settings.worker.pending_payments_check)

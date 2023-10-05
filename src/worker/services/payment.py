import logging
from dataclasses import dataclass

from shared.database.dto import UserPaymentDTO
from shared.exceptions.payments import PaymentExternalApiException
from worker.core.config import Settings
from worker.providers import ProviderFactory
from worker.uow import UnitOfWorkABC

logger = logging.getLogger(__name__)


@dataclass
class PaymentStatusService:
    _provider_factory: ProviderFactory
    _settings: Settings
    _uow: UnitOfWorkABC

    def update_pending_payments(self, delay: int = 5):
        with self._uow:
            payments = self._uow.payment_repo.get_payments_with_status("pending", delay)
            for payment in payments:
                new_status = self._request_new_payment_status(payment)
                if new_status == payment.pay_status.alias:
                    continue
                is_updated = self._uow.payment_repo.set_status(payment.id, new_status)
                if not is_updated:
                    logger.warning("Failed to update payment status for payment ID %s", payment.id)
            self._uow.commit()
            logger.info("Payments checked, next check in %s second(s)", self._settings.worker.pending_payments_check)

    def _request_new_payment_status(self, payment: UserPaymentDTO) -> str:
        provider = self._provider_factory.get_payment_provider(payment.pay_system.alias)
        try:
            new_status = provider.get_payment_status(payment)
        except PaymentExternalApiException:
            new_status = "failed"
            logger.warning("Setting status %s to payment %s due to external api error", new_status, payment.id)
        return new_status

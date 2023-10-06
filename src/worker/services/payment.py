import logging
from dataclasses import dataclass

from shared.constants import EventTypes
from shared.providers.payments.factory import ProviderFactory
from shared.services import EventSenderService
from worker.core.config import Settings
from worker.uow import UnitOfWorkABC

logger = logging.getLogger(__name__)


@dataclass
class PaymentStatusService:
    _provider_factory: ProviderFactory
    _settings: Settings
    _uow: UnitOfWorkABC
    _event_service: EventSenderService

    def update_pending_payments(self):
        with self._uow:
            payments = self._uow.payment_repo.get_payments_with_status("pending", 5)
            for payment in payments:
                provider = self._provider_factory.get_payment_provider(payment.system)
                updated_payment = provider.get_payment_status(payment)
                if not updated_payment:
                    continue
                is_updated = self._uow.payment_repo.set_payment_status(payment)
                if is_updated:
                    payment_data = {
                        "user_id": payment.user_id,
                        "payment_id": updated_payment.id,
                        "payment_status": updated_payment.status,
                    }
                    self._event_service.send_event(event_type=EventTypes.SuccesSubscription, data=payment_data)
                    logger.info(
                        "Updated payment with id %s to status %s",
                        updated_payment.id,
                        updated_payment.status,
                    )
            self._uow.commit()
            logger.info("Payments checked, next check in %s second(s)", self._settings.worker.pending_payments_check)

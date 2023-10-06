import logging
from dataclasses import dataclass
from uuid import UUID

from shared.constants import EventTypes
from shared.database.dto import UserPaymentDTO
from shared.exceptions.payments import PaymentExternalApiException
from shared.services import EventSenderService
from worker.core.config import Settings
from worker.providers import ProviderFactory
from worker.providers.base_provider import BasePaymentProvider
from worker.schemas.status import StatusEnum
from worker.uow import UnitOfWorkABC

logger = logging.getLogger(__name__)


@dataclass
class PaymentStatusService:
    _provider_factory: ProviderFactory
    _settings: Settings
    _uow: UnitOfWorkABC
    _event_service: EventSenderService

    def update_pending_payments_and_activate_subs(self, delay: int = 5):
        with self._uow:
            payments = self._uow.payment_repo.get_payments_with_status("pending", delay)
            for payment in payments:
                provider = self._provider_factory.get_payment_provider(payment.pay_system.alias)
                new_status = self._request_new_payment_status(provider, payment)
                if new_status == payment.pay_status.alias:
                    continue
                is_updated = self._uow.payment_repo.set_status(payment.id, new_status)
                if is_updated:
                    logger.info("Updated payment with id %s to status %s", payment.id, new_status)

                if provider.map_status(new_status) == StatusEnum.succeeded:
                    self._uow.subscription_repo.activate_by_payment_id(payment.id)
                    self._send_event(payment.user_id, payment.id, new_status, EventTypes.SuccesSubscription)

            self._uow.commit()
            logger.info("Payments checked, next check in %s second(s)", self._settings.worker.pending_payments_check)

    def _request_new_payment_status(self, provider: BasePaymentProvider, payment: UserPaymentDTO) -> str:
        try:
            new_status = provider.get_payment_status(payment)
        except PaymentExternalApiException:
            new_status = "failed"
            logger.warning("Setting status %s to payment %s due to external api error", new_status, payment.id)
        return new_status

    def _send_event(self, user_id: UUID, payment_id: UUID, payment_status: str, event_type: EventTypes) -> None:
        payment_data = {
            "user_id": user_id,
            "payment_id": payment_id,
            "payment_status": payment_status,
        }
        self._event_service.send_event(event_type=event_type, data=payment_data)

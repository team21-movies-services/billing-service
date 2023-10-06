import logging
from dataclasses import dataclass

from shared.constants import EventTypes
from shared.providers.payments import ProviderFactory
from shared.services import EventSenderService
from worker.core.config import Settings
from worker.uow import UnitOfWorkABC

logger = logging.getLogger(__name__)


@dataclass
class SubscriptionService:
    _provider_factory: ProviderFactory
    _settings: Settings
    _uow: UnitOfWorkABC
    _event_service: EventSenderService

    def disable(self):
        with self._uow:
            subs = self._uow.subscription_repo.disable()
            self._uow.commit()
            for sub in subs:
                cancel_event_data = {
                    "user_id": sub.user_id,
                    "sub_id": sub.id,
                    "tariff_id": sub.tariff_id,
                }
                self._event_service.send_event(event_type=EventTypes.CancelSubscripton, data=cancel_event_data)
            logger.info("Subscriptions with ids %s disabled.", ", ".join(str(sub.id) for sub in subs))
        logger.info("Subscriptions disable task complete")

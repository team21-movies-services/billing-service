import logging
from dataclasses import dataclass

from worker.core.config import Settings
from worker.providers import ProviderFactory
from worker.uow import UnitOfWorkABC

logger = logging.getLogger(__name__)


@dataclass
class SubscriptionService:
    _provider_factory: ProviderFactory
    _settings: Settings
    _uow: UnitOfWorkABC

    def disable(self):
        with self._uow:
            subscriptions = self._uow.subscription_repo.disable()
            self._uow.commit()
            logger.info(
                "Disabled %s subscriptions: %s",
                len(subscriptions),
                [subscription.id for subscription in subscriptions],
            )
        logger.info("Subscriptions disabled, next disable in %s second(s)", self._settings.worker.disable_subscriptions)

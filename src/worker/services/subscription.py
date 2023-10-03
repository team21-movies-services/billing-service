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
            subs = self._uow.subscription_repo.disable()
            self._uow.commit()
            # TODO: отпарвка события о деактивации подписки
            logger.info("Subscriptions with ids %s disabled.", ", ".join(str(sub.id) for sub in subs))
        logger.info("Subscriptions disable task complete")

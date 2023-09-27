import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.repositories.user_subscription import UserSubscriptionRepositoryABC
from app.services.tariff import TariffServiceABC

logger = logging.getLogger(__name__)


class SubscriptionServiceABC(ABC):
    @abstractmethod
    async def buy(self, pay_system: str, user_id: UUID, tariff_id: UUID):
        raise NotImplementedError


@dataclass
class SubscriptionService(SubscriptionServiceABC):
    _tariff_service: TariffServiceABC
    _user_subscriptions_repository: UserSubscriptionRepositoryABC

    async def buy(self, pay_system: str, user_id: UUID, tariff_id: UUID):
        tariff = await self._tariff_service.get_by_id(tariff_id)
        logger.info(f"Get tariff {tariff}")
        return 1
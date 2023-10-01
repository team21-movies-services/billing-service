import logging
from abc import ABC, abstractmethod
from uuid import UUID

from shared.exceptions.not_exist import PaySystemDoesNotExist, TariffDoesNotExist

from app.schemas.response.subscriptions import UserSubscriptionResponse
from app.uow.subscription_uow import ISubscriptionUoW

logger = logging.getLogger(__name__)


class SubscriptionServiceABC(ABC):
    @abstractmethod
    async def buy(self, pay_system: str, user_id: UUID, tariff_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        raise NotImplementedError


class SubscriptionService(SubscriptionServiceABC):
    def __init__(self, subscription_uow: ISubscriptionUoW):
        self._subscription_uow = subscription_uow

    async def buy(self, pay_system_alias: str, user_id: UUID, tariff_id: UUID):
        async with self._subscription_uow:
            pay_system = await self._subscription_uow.pay_system_repository.get_by_alias(pay_system_alias)
            logger.info(f"Get pay_system '{pay_system}'")
            if not pay_system:
                raise PaySystemDoesNotExist

            tariff = await self._subscription_uow.tariff_repository.get_by_id(tariff_id)
            logger.info(f"Get tariff '{tariff}'")
            if not tariff:
                raise TariffDoesNotExist

            await self._subscription_uow.commit()

        return 1

    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        async with self._subscription_uow:
            return await self._subscription_uow.subscription_repository.get_user_current_subscription(user_id)

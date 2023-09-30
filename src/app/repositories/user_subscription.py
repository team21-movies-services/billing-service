from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from shared.database.models.user_subscription import UserSubscription
from shared.exceptions.base import UserCurrentSubscriptionNotExist
from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from app.repositories.base import SQLAlchemyRepo
from app.schemas.response.subscriptions import UserSubscriptionResponse


class UserSubscriptionRepositoryABC(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        raise NotImplementedError


class UserSubscriptionRepository(SQLAlchemyRepo, UserSubscriptionRepositoryABC):
    async def get_all(self):
        return 1

    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        query = (
            select(UserSubscription)
            .where(UserSubscription.user_id == user_id, UserSubscription.period_end > datetime.now())
            .join(UserSubscription.tariff)
            .options(contains_eager(UserSubscription.tariff))
        )
        result = await self._session.execute(query)
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            raise UserCurrentSubscriptionNotExist
        return UserSubscriptionResponse.model_validate(db_obj)

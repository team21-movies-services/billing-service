from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from shared.database.models.user_subscription import UserSubscription
from shared.exceptions.not_exist import UserCurrentSubscriptionNotExist
from shared.schemas.subscription import SubscriptionAddSchema
from sqlalchemy import desc, insert, not_, select, update
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

    @abstractmethod
    async def cancel_renew_by_user_id(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_subscription(self, subscription_add_schema: SubscriptionAddSchema):
        raise NotImplementedError


class UserSubscriptionRepository(SQLAlchemyRepo, UserSubscriptionRepositoryABC):
    async def get_all(self):
        return 1

    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        query = (
            select(UserSubscription)
            .where(
                UserSubscription.user_id == user_id,
                UserSubscription.period_end > datetime.utcnow(),
                not_(UserSubscription.is_disabled),
            )
            .order_by(desc(UserSubscription.period_start))
            .join(UserSubscription.tariff)
            .options(contains_eager(UserSubscription.tariff))
        )
        result = await self._session.execute(query)
        db_obj = result.scalars().first()
        if not db_obj:
            raise UserCurrentSubscriptionNotExist
        return UserSubscriptionResponse.model_validate(db_obj)

    async def cancel_renew_by_user_id(self, user_id: UUID) -> None:
        query = update(UserSubscription).where(UserSubscription.user_id == user_id).values(renew=False)
        await self._session.execute(query)
        await self._session.commit()

    async def add_subscription(self, subscription_add_schema: SubscriptionAddSchema):
        stmt = insert(UserSubscription).values(**subscription_add_schema.model_dump()).returning(UserSubscription)
        result = await self._session.execute(stmt)
        if user_payment := result.scalar():
            return user_payment
        return None

from abc import ABC, abstractmethod

from app.repositories.base import SQLAlchemyRepo


class UserSubscriptionRepositoryABC(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError


class UserSubscriptionRepository(SQLAlchemyRepo, UserSubscriptionRepositoryABC):
    async def get_all(self):
        return 1

from abc import ABC, abstractmethod
from uuid import UUID

from shared.database.models.tariff import Tariff

from app.repositories.base import SQLAlchemyRepo


class TariffRepositoryABC(ABC):
    @abstractmethod
    async def get_by_id(self, tariff_id: UUID) -> Tariff | None:
        raise NotImplementedError


class TariffRepository(SQLAlchemyRepo, TariffRepositoryABC):
    async def get_by_id(self, tariff_id: UUID) -> Tariff | None:
        return await self._session.get(Tariff, tariff_id)

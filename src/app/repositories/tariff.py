from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from shared.database.models.tariff import Tariff
from sqlalchemy import select

from app.repositories.base import SQLAlchemyRepo


class TariffRepositoryABC(ABC):
    @abstractmethod
    async def get_by_id(self, tariff_id: UUID) -> Tariff | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Sequence[Tariff]:
        raise NotImplementedError


class TariffRepository(SQLAlchemyRepo, TariffRepositoryABC):
    async def get_by_id(self, tariff_id: UUID) -> Tariff | None:
        return await self._session.get(Tariff, tariff_id)

    async def get_all(self) -> Sequence[Tariff]:
        result = await self._session.execute(select(Tariff).order_by(Tariff.cost))
        return result.scalars().all()

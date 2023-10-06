from abc import ABC, abstractmethod

from shared.database.models.pay_system import PaySystem
from sqlalchemy.sql import select

from app.repositories.base import SQLAlchemyRepo
from app.schemas.response.pay_system import PaySystemResponse


class PaySystemRepositoryABC(ABC):
    @abstractmethod
    async def get_all(self) -> list[PaySystemResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_alias(self, pay_system_alias: str) -> PaySystemResponse | None:
        raise NotImplementedError


class PaySystemRepository(SQLAlchemyRepo, PaySystemRepositoryABC):
    async def get_all(self) -> list[PaySystemResponse]:
        query_result = await self._session.execute(select(PaySystem))
        db_objs = query_result.scalars().all()
        return [PaySystemResponse.model_validate(db_obj) for db_obj in db_objs]

    async def get_by_alias(self, pay_system_alias: str) -> PaySystemResponse | None:
        stmt = select(PaySystem).filter_by(alias=pay_system_alias)
        result = await self._session.execute(stmt)
        response = result.scalar()
        if not response:
            return None
        return PaySystemResponse.model_validate(response)

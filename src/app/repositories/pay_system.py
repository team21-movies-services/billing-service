from abc import ABC, abstractmethod

from shared.database.models.pay_system import PaySystem
from sqlalchemy.sql import select

from app.repositories.base import SQLAlchemyRepo
from app.schemas.response.pay_system import PaySystemResponse


class PaySystemRepositoryABC(ABC):
    @abstractmethod
    async def get_all(self) -> list[PaySystemResponse]:
        raise NotImplementedError


class PaySystemRepository(SQLAlchemyRepo, PaySystemRepositoryABC):
    async def get_all(self) -> list[PaySystemResponse]:
        query_result = await self._session.execute(select(PaySystem))
        db_objs = query_result.scalars().all()
        return [PaySystemResponse.model_validate(db_obj) for db_obj in db_objs]

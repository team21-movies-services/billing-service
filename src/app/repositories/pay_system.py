from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from models.pay_system import PaySystem
from schemas.response.pay_system import PaySystemResponse


class PaySystemRepositoryABC(ABC):
    @abstractmethod
    async def get_all(self) -> list[PaySystemResponse]:
        raise NotImplementedError


class PaySystemRepository(PaySystemRepositoryABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> list[PaySystemResponse]:
        query_result = await self._session.execute(select(PaySystem))
        db_objs = query_result.scalars().all()
        return [PaySystemResponse.model_validate(db_obj) for db_obj in db_objs]

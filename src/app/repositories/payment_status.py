from abc import ABC, abstractmethod

from shared.database.models.pay_status import PayStatus
from sqlalchemy import select

from app.repositories.base import SQLAlchemyRepo
from app.schemas.domain.payment_status import PaymentStatus


class PaymentStatusRepositoryABC(ABC):
    @abstractmethod
    async def get_by_alias(self, status_alias: str) -> PaymentStatus | None:
        raise NotImplementedError


class PaymentStatusRepository(SQLAlchemyRepo, PaymentStatusRepositoryABC):
    async def get_by_alias(self, status_alias: str) -> PaymentStatus | None:
        stmt = select(PayStatus).filter_by(alias=status_alias)
        result = await self._session.execute(stmt)
        if status := result.scalar():
            return PaymentStatus(
                id=status.id,
                name=status.name,
                alias=status.alias,
            )
        return None

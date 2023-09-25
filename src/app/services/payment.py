from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.repositories.payment import PaymentRepositoryABC
from app.schemas.request.pagination import PaymentsPagination
from app.schemas.response.payment import UserPaymentResponse


class PaymentServiceABC(ABC):
    @abstractmethod
    async def get_all_by_user_id(self, user_id: UUID, pagination: PaymentsPagination) -> list[UserPaymentResponse]:
        raise NotImplementedError


@dataclass
class PaymentService(PaymentServiceABC):
    _payment_repository: PaymentRepositoryABC

    async def get_all_by_user_id(self, user_id: UUID, pagination: PaymentsPagination) -> list[UserPaymentResponse]:
        return await self._payment_repository.get_all_by_user_id(user_id, pagination)

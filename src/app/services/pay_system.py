from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.repositories.pay_system import PaySystemRepositoryABC
from app.schemas.response.pay_system import PaySystemResponse


class PaySystemServiceABC(ABC):
    @abstractmethod
    async def get_pay_systems_list(self) -> list[PaySystemResponse]:
        raise NotImplementedError


@dataclass
class PaySystemService(PaySystemServiceABC):
    _pay_systems_repository: PaySystemRepositoryABC

    async def get_pay_systems_list(self) -> list[PaySystemResponse]:
        return await self._pay_systems_repository.get_all()

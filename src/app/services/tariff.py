from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from shared.exceptions.base import TariffDoesNotExist

from app.repositories.tariff import TariffRepositoryABC
from app.schemas.response.tariff import TariffResponse


class TariffServiceABC(ABC):
    @abstractmethod
    async def get_by_id(self, tariff_id: UUID) -> TariffResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[TariffResponse]:
        raise NotImplementedError


@dataclass
class TariffService(TariffServiceABC):
    _tariff_repository: TariffRepositoryABC

    async def get_by_id(self, tariff_id: UUID) -> TariffResponse:
        tariff = await self._tariff_repository.get_by_id(tariff_id)
        if not tariff:
            raise TariffDoesNotExist
        return TariffResponse.model_validate(tariff)

    async def get_all(self) -> list[TariffResponse]:
        tariffs = await self._tariff_repository.get_all()
        return [TariffResponse.model_validate(tariff) for tariff in tariffs]

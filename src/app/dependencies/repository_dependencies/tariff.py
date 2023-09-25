from typing import Annotated

from fastapi import Depends

from app.dependencies.clients.db_session import DbSessionDep
from app.repositories.tariff import TariffRepository, TariffRepositoryABC


def get_tariff_repository(session: DbSessionDep) -> TariffRepository:
    return TariffRepository(session)


TariffRepositoryDep = Annotated[TariffRepositoryABC, Depends(get_tariff_repository)]

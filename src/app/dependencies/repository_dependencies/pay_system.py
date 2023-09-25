from typing import Annotated

from fastapi import Depends

from dependencies.clients.db_session import DbSessionDep
from repositories.pay_system import PaySystemRepository, PaySystemRepositoryABC


def get_pay_system_repository(session: DbSessionDep) -> PaySystemRepository:
    return PaySystemRepository(session)


PaySystemRepositoryDep = Annotated[PaySystemRepositoryABC, Depends(get_pay_system_repository)]

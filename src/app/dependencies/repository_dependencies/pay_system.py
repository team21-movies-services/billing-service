from typing import Annotated

from fastapi import Depends

from app.dependencies.clients.db_session import DbSessionDep
from app.repositories.pay_system import PaySystemRepository, PaySystemRepositoryABC


def get_pay_system_repository(session: DbSessionDep) -> PaySystemRepository:
    return PaySystemRepository(session)


PaySystemRepositoryDep = Annotated[PaySystemRepositoryABC, Depends(get_pay_system_repository)]

from typing import Annotated

from fastapi import Depends

from app.dependencies.clients.db_session import DbSessionDep
from app.repositories.payment import PaymentRepository, PaymentRepositoryABC


def get_payment_repository(session: DbSessionDep) -> PaymentRepository:
    return PaymentRepository(session)


PaymentRepositoryDep = Annotated[PaymentRepositoryABC, Depends(get_payment_repository)]

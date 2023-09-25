from typing import Annotated

from fastapi import Depends

from app.dependencies.clients.db_session import DbSessionDep
from app.repositories.user_subscription import (
    UserSubscriptionRepository,
    UserSubscriptionRepositoryABC,
)


def get_subscription_repository(session: DbSessionDep) -> UserSubscriptionRepository:
    return UserSubscriptionRepository(session)


SubscriptionRepositoryDep = Annotated[UserSubscriptionRepositoryABC, Depends(get_subscription_repository)]

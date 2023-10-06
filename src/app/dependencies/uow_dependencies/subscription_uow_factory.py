from typing import Annotated

from fastapi import Depends

from app.dependencies.clients.db_session import DbSessionMakerDep
from app.uow.subscription_uow import SubscriptionUoW


def create_task_uow(session_maker: DbSessionMakerDep):
    return SubscriptionUoW(session_maker)


SubscriptionUoWDep = Annotated[SubscriptionUoW, Depends(create_task_uow)]

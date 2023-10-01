from app.dependencies.registrator import add_factory_to_mapper
from app.dependencies.uow_dependencies.subscription_uow_factory import (
    SubscriptionUoWDep,
)
from app.services.subscription import SubscriptionService, SubscriptionServiceABC


@add_factory_to_mapper(SubscriptionServiceABC)
def create_subscription_service(subscription_uow: SubscriptionUoWDep) -> SubscriptionService:
    return SubscriptionService(subscription_uow)

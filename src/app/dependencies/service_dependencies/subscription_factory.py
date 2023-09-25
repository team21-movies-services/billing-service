from fastapi import Depends

from app.dependencies.registrator import add_factory_to_mapper
from app.dependencies.repository_dependencies.user_subscription import (
    SubscriptionRepositoryDep,
)
from app.services.subscription import SubscriptionService, SubscriptionServiceABC
from app.services.tariff import TariffServiceABC


@add_factory_to_mapper(SubscriptionServiceABC)
def create_subscription_service(
    subscription_repository: SubscriptionRepositoryDep,
    tariff_service: TariffServiceABC = Depends(),
) -> SubscriptionService:
    return SubscriptionService(tariff_service, subscription_repository)

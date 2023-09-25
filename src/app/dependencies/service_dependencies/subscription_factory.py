from app.dependencies.registrator import add_factory_to_mapper
from app.dependencies.repository_dependencies.user_subscription import (
    SubscriptionRepositoryDep,
)
from app.dependencies.service_dependencies.tariff_factory import TariffServiceDep
from app.services.subscription import SubscriptionService, SubscriptionServiceABC


@add_factory_to_mapper(SubscriptionServiceABC)
def create_subscription_service(
    subscription_repository: SubscriptionRepositoryDep,
    tariff_service: TariffServiceDep,
) -> SubscriptionService:
    return SubscriptionService(tariff_service, subscription_repository)

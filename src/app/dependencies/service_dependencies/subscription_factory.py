from fastapi import Depends
from shared.providers.payments import MockPaymentProvider, YookassaPaymentProvider
from shared.providers.payments.factory import ProviderFactory

from app.core.config import Settings
from app.dependencies.registrator import add_factory_to_mapper
from app.dependencies.settings import get_settings
from app.dependencies.uow_dependencies.subscription_uow_factory import (
    SubscriptionUoWDep,
)
from app.services.subscription import SubscriptionService, SubscriptionServiceABC


@add_factory_to_mapper(SubscriptionServiceABC)
def create_subscription_service(
    subscription_uow: SubscriptionUoWDep,
    settings: Settings = Depends(get_settings),
) -> SubscriptionService:
    yookassa_provider = YookassaPaymentProvider(settings.yookassa)
    mock_payment_provider = MockPaymentProvider()
    payment_provider_factory = ProviderFactory(yookassa_provider, mock_payment_provider)
    return SubscriptionService(subscription_uow, payment_provider_factory)

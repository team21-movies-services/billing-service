from dataclasses import dataclass

from worker.clients.database.pg_client import SQLAlchemyProvider
from worker.providers.factory import ProviderFactory
from worker.schemas.subscription import SubscriptionSchema


@dataclass
class SubscriptionRepository:
    _event_handler: ProviderFactory
    _client: SQLAlchemyProvider

    def get_subscriptions_expires_in(self, days: int = 0) -> SubscriptionSchema:
        ...

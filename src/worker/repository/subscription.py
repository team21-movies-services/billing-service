from dataclasses import dataclass

from worker.clients.database.pg_client import SQLAlchemyProvider
from worker.event_handler import EventHandler
from worker.schemas.subscription import SubscriptionSchema


@dataclass
class SubscriptionRepository:
    _event_handler: EventHandler
    _client: SQLAlchemyProvider

    def get_subscriptions_expires_in(self, days: int = 0) -> SubscriptionSchema:
        ...

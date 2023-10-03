from dataclasses import dataclass

from sqlalchemy.orm import Session
from worker.schemas import SubscriptionSchema


@dataclass
class SubscriptionRepository:
    _session: Session

    def get_subscriptions_expires_in(self, days: int = 0) -> SubscriptionSchema:
        ...

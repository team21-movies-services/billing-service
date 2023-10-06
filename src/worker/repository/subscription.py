from dataclasses import dataclass
from datetime import datetime

from shared.database.models import UserSubscription
from sqlalchemy import not_, or_, update
from sqlalchemy.orm import Session
from worker.schemas.subscription import SubscriptionSchema


@dataclass
class SubscriptionRepository:
    _session: Session

    def get_subscriptions_expires_in(self, days: int = 0) -> SubscriptionSchema:
        ...

    def disable(self) -> list[SubscriptionSchema]:
        query = (
            update(UserSubscription)
            .where(UserSubscription.period_end < datetime.utcnow(), not_(UserSubscription.is_disabled))
            .where(or_(not_(UserSubscription.renew), UserSubscription.renew_try_count >= 3))
            .values(is_disabled=True)
            .returning(UserSubscription)
        )
        results = self._session.execute(query)
        db_objs = results.scalars().all()

        return [SubscriptionSchema.model_validate(db_obj) for db_obj in db_objs]

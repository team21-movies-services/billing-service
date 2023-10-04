import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator

from shared.database.dto import UserSubscriptionDTO
from shared.database.models import UserSubscription
from sqlalchemy import and_, not_, or_, select, update
from sqlalchemy.orm import Session
from worker.schemas import SubscriptionSchema


@dataclass
class SubscriptionRepository:
    _session: Session

    def get_subscriptions_expires_in(
        self,
        days: int = 0,
        batch_size: int = 10,
    ) -> Generator[list[UserSubscriptionDTO], None, None]:
        target_date = datetime.utcnow() + timedelta(days=days)
        conditions = [
            UserSubscription.period_end < target_date,
            UserSubscription.renew_try_count <= 3,
            UserSubscription.renew == True,  # noqa: E712
        ]
        iteration = 0
        while True:
            query = (
                select(UserSubscription)
                .join(UserSubscription.user_payment)
                .join(UserSubscription.tariff)
                .where(and_(*conditions))
                .with_for_update(of=UserSubscription, skip_locked=True)
                .limit(batch_size)
                .offset(batch_size * iteration)
            )
            scalars = self._session.execute(query).scalars()
            results = [UserSubscriptionDTO.model_validate(result) for result in scalars]
            logging.debug(results)
            if not results:
                break
            yield results
            iteration += 1

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

    def increment_subscription_retries(self, subscription: UserSubscriptionDTO) -> int:
        query = select(UserSubscription).where(UserSubscription.id == subscription.id)
        sub = self._session.execute(query).scalar_one()
        sub.renew_try_count += 1
        retries = sub.renew_try_count
        logging.info("Incrementing subscription %s renew tries count, new value %s", subscription.id, retries)
        return retries

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator

from shared.database.dto import UserSubscriptionDTO
from shared.database.models import UserSubscription
from shared.database.models.tariff import TariffPeriodUnit
from sqlalchemy import and_, not_, or_, select, update
from sqlalchemy.orm import Session
from worker.schemas import SubscriptionSchema

logger = logging.getLogger(__name__)


@dataclass
class SubscriptionRepository:
    _session: Session

    def get_subscriptions_for_renew(
        self,
    ) -> Generator[UserSubscriptionDTO, None, None]:
        current_date = datetime.utcnow()
        target_date = current_date - timedelta(hours=6)
        conditions = [
            UserSubscription.period_end < current_date,
            UserSubscription.renew_try_count <= 3,
            UserSubscription.renew == True,  # noqa: E712
            or_(UserSubscription.last_check < target_date, UserSubscription.last_check == None),  # noqa: E711
        ]
        logger.info("Checking subscriptions for renew")
        while True:
            query = (
                select(UserSubscription)
                .join(UserSubscription.user_payment)
                .join(UserSubscription.tariff)
                .where(and_(*conditions))
                .with_for_update(of=UserSubscription, skip_locked=True)
                .limit(1)
            )
            query_result = self._session.execute(query).scalar_one_or_none()
            if query_result is None:
                logger.info("No subscriptions for renew")
                break
            subscription = UserSubscriptionDTO.model_validate(query_result)
            yield subscription

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

    def increment_retries(self, subscription: UserSubscriptionDTO, reset: bool = False) -> int:
        query = select(UserSubscription).where(UserSubscription.id == subscription.id)
        sub = self._session.execute(query).scalar_one()

        if reset:
            sub.renew_try_count = 0
            retries = sub.renew_try_count
        else:
            sub.renew_try_count += 1
            retries = sub.renew_try_count
            logger.info("Incrementing subscription %s renew tries count, new value %s", subscription.id, retries)
        return retries

    def update_end_period(self, subscription: UserSubscriptionDTO) -> UserSubscriptionDTO:
        to_days_map = {
            TariffPeriodUnit.day: 1,
            TariffPeriodUnit.month: 30,
            TariffPeriodUnit.year: 365,
        }
        tariff_period = timedelta(days=to_days_map[subscription.tariff.period_unit])

        query = select(UserSubscription).where(UserSubscription.id == subscription.id)
        subscription_obj = self._session.execute(query).scalar_one()
        subscription_obj.period_end += tariff_period
        logger.info("Updated end period for subscription %s", subscription.id)
        return UserSubscriptionDTO.model_validate(subscription_obj)

    def update_last_checked(self, subscription: UserSubscriptionDTO):
        current_time = datetime.utcnow()
        query = update(UserSubscription).where(UserSubscription.id == subscription.id).values(last_check=current_time)
        logger.info("Setting last checked date for subscription %s", subscription.id)
        self._session.execute(query)

    def disable_one(self, subscription: UserSubscriptionDTO):
        query = update(UserSubscription).where(UserSubscription.id == subscription.id).values(disabled=True)
        logger.info("Disabling subscription %s", subscription.id)
        self._session.execute(query)

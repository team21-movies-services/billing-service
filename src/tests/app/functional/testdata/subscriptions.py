from datetime import datetime, timedelta
from uuid import UUID, uuid4

from faker import Faker
from shared.database.models.user_subscription import UserSubscription

fake = Faker('ru_RU')


def fake_subscription(tariff_id: UUID, user_payment_id: UUID, user_id: UUID) -> UserSubscription:
    data = dict(
        id=uuid4(),
        tariff_id=tariff_id,
        user_payment_id=user_payment_id,
        user_id=user_id,
        period_start=datetime.utcnow(),
        period_end=datetime.utcnow() + timedelta(days=30),
        is_disabled=False,
        renew=False,
        renew_try_count=0,
    )
    return UserSubscription(**data)


def fake_renew_subscription(tariff_id: UUID, user_payment_id: UUID, user_id: UUID) -> UserSubscription:
    subscription = fake_subscription(tariff_id, user_payment_id, user_id)
    subscription.renew = True
    return subscription

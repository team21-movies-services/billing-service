from uuid import UUID, uuid4

from faker import Faker
from shared.database.models.user_payment import UserPayment

fake = Faker('ru_RU')


def fake_user_payment(pay_system_id: UUID, pay_status_id: UUID, user_id: UUID) -> UserPayment:
    data = dict(
        id=uuid4(),
        pay_system_id=pay_system_id,
        pay_status_id=pay_status_id,
        user_id=user_id,
        payment_id=uuid4(),
        amount=90,
        purpose="Subscription",
        json_detail={},
    )
    return UserPayment(**data)

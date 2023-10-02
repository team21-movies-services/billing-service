from uuid import uuid4

from faker import Faker
from shared.database.models.pay_status import PayStatus

fake = Faker('ru_RU')


def fake_pay_status() -> PayStatus:
    data = dict(
        id=uuid4(),
        name=fake.word(),
        alias=fake.word(),
    )
    return PayStatus(**data)

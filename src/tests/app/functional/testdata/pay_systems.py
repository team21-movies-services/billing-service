from uuid import uuid4

from faker import Faker
from shared.database.models.pay_system import PaySystem

fake = Faker('ru_RU')


def fake_pay_system() -> PaySystem:
    data = dict(
        id=uuid4(),
        name=fake.word(),
        alias=fake.word(),
        currency_code="RUB",
        json_data={},
    )
    return PaySystem(**data)

from datetime import datetime
from uuid import uuid4

from faker import Faker
from shared.database.models.tariff import Tariff, TariffPeriodUnit

fake = Faker('ru_RU')


def fake_tariff() -> Tariff:
    data = dict(
        id=uuid4(),
        name=fake.name(),
        alias=fake.word(),
        cost=fake.random_int(min=50, max=100),
        period=fake.random_int(min=1, max=12),
        period_unit=fake.enum(TariffPeriodUnit),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    return Tariff(**data)

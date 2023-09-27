import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from tests.app.functional.testdata.tariffs import fake_tariff


@pytest_asyncio.fixture()
async def tariffs(db_session: AsyncSession):
    _tariffs = [fake_tariff() for _ in range(5)]
    db_session.add_all(_tariffs)
    await db_session.commit()
    yield _tariffs
    for tariff in _tariffs:
        await db_session.delete(tariff)

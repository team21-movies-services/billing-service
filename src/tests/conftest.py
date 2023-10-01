import asyncio

import pytest
import pytest_asyncio
from shared.database.models.base import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils import create_database, drop_database

from app.core.config import settings

pytest_plugins = (
    "tests.app.functional.plugins.api_client",
    "tests.app.functional.plugins.auth_user",
    "tests.app.functional.plugins.create_data",
    "tests.testdata.user_payments",
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _create_test_db():
    create_database(settings.postgres.database_url)
    yield
    drop_database(settings.postgres.database_url)


@pytest_asyncio.fixture(name='db_session', scope="session")
async def db_session_with_migrations(_create_test_db):
    engine = create_async_engine(settings.postgres.database_url)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        # есть ощущение что этот ENUM еще даст о себе вспомнить)
        await conn.execute(text("CREATE TYPE tariff_period_unit AS ENUM ('day', 'month', 'year')"))
        await conn.run_sync(BaseModel.metadata.create_all)
    async with session_maker() as session:
        yield session
    await engine.dispose()

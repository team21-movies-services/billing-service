import asyncio

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils import create_database, drop_database

from app.core.config import settings

pytest_plugins = (
    "tests.app.functional.plugins.api_client",
    "tests.app.functional.plugins.auth_user",
    "tests.app.functional.plugins.create_data",
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
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.postgres.database_url)
    command.upgrade(alembic_cfg, "head")
    async with session_maker() as session:
        yield session
    await engine.dispose()

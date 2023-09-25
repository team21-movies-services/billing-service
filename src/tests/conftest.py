import asyncio
import time

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils import create_database, drop_database

from core.config import settings

pytest_plugins = (
    "tests.app.functional.plugins.api_client",
    "tests.app.functional.plugins.auth_user",
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
    # assert settings.postgres.database_url == "test_billing_database"
    engine = create_async_engine(settings.postgres.database_url)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.postgres.database_url)
    command.upgrade(alembic_cfg, "head")
    async with session_maker() as session:
        yield session
    await engine.dispose()


@pytest.fixture(scope="module")
def single_use_database():
    """
    SQLAlchemy engine, for single use
    """
    timestamp = str(int(time.time()))
    db_url = settings.postgres.database_url + timestamp
    create_database(db_url)
    engine = create_engine(db_url, echo=True)
    try:
        yield engine
    finally:
        engine.dispose()
        drop_database(db_url)

import time

import pytest
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database

from core.config import settings


@pytest.fixture()
def alembic_config():
    return Config("alembic.ini")


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

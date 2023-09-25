import pytest
from alembic.config import Config


@pytest.fixture()
def alembic_config():
    return Config("alembic.ini")

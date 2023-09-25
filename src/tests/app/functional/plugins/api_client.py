import pytest_asyncio
from httpx import AsyncClient

from dependencies.auth import get_auth_data
from dependencies.clients.db_session import get_db_session
from main import app


@pytest_asyncio.fixture(name="api_client", scope='module')
async def client_fixture(auth_user, db_session):
    def get_session_override():
        return db_session

    def get_auth_override():
        return auth_user

    app.dependency_overrides[get_auth_data] = get_auth_override
    app.dependency_overrides[get_db_session] = get_session_override

    async with AsyncClient(app=app, base_url="http://test", headers={"X-Request-Id": '123'}) as client:
        yield client

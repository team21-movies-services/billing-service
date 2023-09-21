import pytest_asyncio
from httpx import AsyncClient

from dependencies.auth import get_auth_data
from main import app


@pytest_asyncio.fixture(name="api_client", scope='session')
async def client_fixture(auth_user):
    def get_auth_override():
        return auth_user

    app.dependency_overrides[get_auth_data] = get_auth_override

    async with AsyncClient(app=app, base_url="http://test", headers={"X-Request-Id": '123'}) as client:
        yield client

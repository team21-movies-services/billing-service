from uuid import uuid4

import pytest_asyncio

from dependencies.auth import get_auth_data
from main import app
from schemas.domain.auth import AuthData


@pytest_asyncio.fixture(name='auth_user', scope='session')
async def auth_user_fixture():
    yield AuthData(user_id=uuid4(), is_superuser=False)


@pytest_asyncio.fixture(name='access_token', scope='function')
async def access_token_fixture(auth_user: AuthData, get_access_token: str):
    """Enable auth and return normal access token than disable auth"""

    def get_auth_override():
        return auth_user

    app.dependency_overrides[get_auth_data] = get_auth_data
    yield get_access_token
    app.dependency_overrides[get_auth_data] = get_auth_override


@pytest_asyncio.fixture(name='forbidden_access_token', scope='function')
async def forbidden_token_fixture(auth_user: AuthData, get_forbidden_token: str):
    """Enable auth and return bad access token than disable auth"""

    def get_auth_override():
        return auth_user

    app.dependency_overrides[get_auth_data] = get_auth_data
    yield get_forbidden_token
    app.dependency_overrides[get_auth_data] = get_auth_override


@pytest_asyncio.fixture(name='expire_access_token', scope='function')
async def expire_token_fixture(auth_user: AuthData, get_expire_token: str):
    """Enable auth and return expire access token than disable auth"""

    def get_auth_override():
        return auth_user

    app.dependency_overrides[get_auth_data] = get_auth_data
    yield get_expire_token
    app.dependency_overrides[get_auth_data] = get_auth_override

import pytest_asyncio
from httpx import AsyncClient

# from dependencies.clients.get_db_session import get_db_session
from dependencies.auth import get_auth_data
from core.config import settings
from main import app

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


@pytest_asyncio.fixture(name="db_session", scope="session")
async def db_session():
    engine = create_async_engine(settings.postgres.database_url)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with session_maker() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture(name="api_client", scope='session')
async def client_fixture(auth_user, db_session):
    def get_session_override():
        return db_session

    def get_auth_override():
        return auth_user

    app.dependency_overrides[get_auth_data] = get_auth_override
    # app.dependency_overrides[get_db_session] = get_session_override

    async with AsyncClient(app=app, base_url="http://test", headers={"X-Request-Id": '123'}) as client:
        yield client

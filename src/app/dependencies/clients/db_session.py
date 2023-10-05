from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import Settings
from app.dependencies.settings import get_settings
from app.providers.pg_providers import SQLAlchemyProvider


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    app: FastAPI = request.app
    session_maker = app.state.async_session_maker
    session = session_maker()
    try:
        yield session
    finally:
        await session.commit()
        await session.close()


async def get_db_session_maker(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    app: FastAPI = request.app
    sa_provider = SQLAlchemyProvider(
        app=app,
        async_dns=settings.postgres.database_url,
        echo_log=settings.postgres.echo_log,
    )
    session_maker = sa_provider.async_session_maker
    return session_maker


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
DbSessionMakerDep = Annotated[async_sessionmaker[AsyncSession], Depends(get_db_session_maker)]

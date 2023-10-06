from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession


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


async def get_db_session_maker(request: Request):
    app: FastAPI = request.app
    session_maker = app.state.async_session_maker
    return session_maker


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
DbSessionMakerDep = Annotated[AsyncSession, Depends(get_db_session_maker)]

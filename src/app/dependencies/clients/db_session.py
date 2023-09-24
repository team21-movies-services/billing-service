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
        await session.close()


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

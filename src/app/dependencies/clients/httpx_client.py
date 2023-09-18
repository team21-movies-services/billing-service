from typing import AsyncGenerator

from fastapi import FastAPI, Request
from httpx import AsyncClient


async def get_httpx_client(request: Request) -> AsyncGenerator[AsyncClient, None]:
    app: FastAPI = request.app
    http_client: AsyncClient = app.state.async_http_client
    yield http_client

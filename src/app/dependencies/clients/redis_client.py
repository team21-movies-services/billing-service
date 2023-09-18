from typing import AsyncGenerator

from fastapi import FastAPI, Request
from redis.asyncio import Redis


async def get_redis_client(
    request: Request,
) -> AsyncGenerator[Redis, None]:
    app: FastAPI = request.app
    redis_client: Redis = app.state.async_redis_client
    try:
        yield redis_client
    finally:
        await redis_client.close()

import logging

from fastapi import FastAPI

from app.core.config import Settings
from app.providers.cache_providers import RedisProvider
from app.providers.http_providers import HTTPXClientProvider
from app.providers.pg_providers import SQLAlchemyProvider

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, settings: Settings):
    redis_provider = RedisProvider(
        app=app,
        host=settings.redis.host,
        port=settings.redis.port,
    )
    redis_provider.register_events()
    logger.info(f"Setup Redis Provider. host:port: {settings.redis.host}:{settings.redis.port}")

    http_client = HTTPXClientProvider(app=app)
    http_client.register_events()
    logger.info(f"Setup Http Provider. {http_client}")

    sa_provider = SQLAlchemyProvider(
        app=app,
        async_dns=settings.postgres.database_url,
        echo_log=settings.postgres.echo_log,
    )
    sa_provider.register_events()
    logger.info(f"Setup SQLAlchemy Provider. DSN: {settings.postgres.database_url}")

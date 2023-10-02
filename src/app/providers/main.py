import logging

from fastapi import FastAPI

from app.core.config import Settings
from app.providers.admin_provider import AdminProvider
from app.providers.cache_providers import RedisProvider
from app.providers.http_providers import HTTPXClientProvider
from app.providers.pg_providers import SQLAlchemyProvider
from app.providers.sentry_provider import SentryProvider

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

    admin_provider = AdminProvider(
        app=app,
        settings=settings.admin,
        session_maker=sa_provider.async_session_maker,
    )
    admin_provider.register_events()
    logger.info("Setup Admin Provider.")

    if settings.sentry.enable:
        sentry_provider = SentryProvider(app=app, dsn=settings.sentry.dsn)
        sentry_provider.register_events()
        logger.info("Setup Sentry Provider.")

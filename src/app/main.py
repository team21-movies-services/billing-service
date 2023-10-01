from logging import config as logging_config

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.routers.main import setup_routers
from app.core.config import Settings
from app.core.logger import LOGGING
from app.dependencies.main import setup_dependencies
from app.exceptions.main import setup_error_handlers
from app.middleware.main import setup_middleware
from app.providers.main import setup_providers

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.project.name,
        docs_url='/docs',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        description="Billing system for online movies service",
        version="0.1.0",
    )
    setup_providers(app, settings)
    setup_routers(app)
    setup_dependencies(app)
    setup_middleware(app)
    setup_error_handlers(app)
    return app


settings = Settings()
app = create_app(settings)

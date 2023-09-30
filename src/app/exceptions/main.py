import logging

from fastapi import FastAPI
from shared.exceptions.base import BaseError

from app.exceptions.base import BaseAppException

from .error_handlers import application_exception_handler, shared_exception_handler

logger = logging.getLogger(__name__)


def setup_error_handlers(app: FastAPI):
    app.add_exception_handler(BaseAppException, application_exception_handler)
    logger.info("Setup %s error handler", BaseAppException)

    app.add_exception_handler(BaseError, shared_exception_handler)
    logger.info("Setup %s error handler", BaseError)

import logging

from fastapi import FastAPI
from shared.exceptions.base import BaseError

from app.exceptions.base import AppException

from .error_handlers import application_exception_handler, shared_exception_handler

logger = logging.getLogger(__name__)


def setup_error_handlers(app: FastAPI):
    app.add_exception_handler(AppException, application_exception_handler)
    logger.info("Setup %s error handler", AppException)

    app.add_exception_handler(BaseError, shared_exception_handler)
    logger.info("Setup %s error handler", BaseError)

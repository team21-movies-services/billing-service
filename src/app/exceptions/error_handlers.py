import logging

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from shared.exceptions import base as shared_exceptions

from app.exceptions import base as app_exceptions

logger = logging.getLogger(__name__)


async def application_exception_handler(request: Request, exc: app_exceptions.BaseAppException):
    answer = {
        "code": exc.code,
        "error": exc.error,
        "detail": exc.detail,
    }

    if isinstance(exc, app_exceptions.BaseAuthException):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, app_exceptions.BaseClientException):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif isinstance(exc, app_exceptions.BaseForbiddenException):
        status_code = status.HTTP_403_FORBIDDEN
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    logger.exception(exc, exc_info=exc)

    return JSONResponse(status_code=status_code, content=jsonable_encoder(answer))


async def shared_exception_handler(request: Request, exc: shared_exceptions.BaseError):
    answer = {
        "code": exc.code,
        "error": exc.error,
        "detail": exc.detail,
    }

    if isinstance(exc, shared_exceptions.BaseDoesNotExist):
        status_code = status.HTTP_404_NOT_FOUND
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    logger.exception(exc, exc_info=exc)

    return JSONResponse(status_code=status_code, content=jsonable_encoder(answer))

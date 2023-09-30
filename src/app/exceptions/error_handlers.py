from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from shared.exceptions import base as shared_exceptions

from app.exceptions import base as app_exceptions


async def application_exception_handler(request: Request, exc: app_exceptions.AppException):
    answer = {"error": exc}

    if isinstance(exc, app_exceptions.AuthException):
        status_code = status.HTTP_401_UNAUTHORIZED
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(status_code=status_code, content=jsonable_encoder(answer))


async def shared_exception_handler(request: Request, exc: shared_exceptions.BaseError):
    answer = {"error": exc}

    if isinstance(exc, shared_exceptions.BaseDoesNotExist):
        status_code = status.HTTP_404_NOT_FOUND
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(status_code=status_code, content=jsonable_encoder(answer))

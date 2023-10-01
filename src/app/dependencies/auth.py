import logging
from typing import Optional

from fastapi import Depends, Security
from fastapi.security import APIKeyHeader

from app.exceptions.base import BaseForbiddenException
from app.schemas.domain.auth import AuthData
from app.services import AuthServiceABC

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

logger = logging.getLogger().getChild('auth')


async def get_auth_data(
    auth_service: AuthServiceABC = Depends(),
    access_token: Optional[str] = Security(api_key_header),
):
    if not access_token:
        raise BaseForbiddenException

    auth_data: AuthData = await auth_service.validate_access_token(access_token)
    logger.debug(f'User request: user_id - {auth_data.user_id}')
    return auth_data


async def get_auth_admin(
    auth_data: AuthData = Depends(get_auth_data),
):
    if not auth_data.is_superuser:
        raise BaseForbiddenException
    return auth_data

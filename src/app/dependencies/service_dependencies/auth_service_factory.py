from fastapi import Depends

from core.config import Settings
from dependencies.registrator import add_factory_to_mapper
from dependencies.settings import get_settings
from services.auth import AuthService, AuthServiceABC


@add_factory_to_mapper(AuthServiceABC)
def create_auth_service(
    settings: Settings = Depends(get_settings),
):
    return AuthService(
        jwt_secret_key=settings.project.jwt_secret_key,
    )

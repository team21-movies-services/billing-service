from http import HTTPStatus

from fastapi import FastAPI, Request
from httpx import AsyncClient
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.api.routers.admin import (
    PaymentsAdminView,
    SubscriptionsAdminView,
    TariffsAdminView,
)
from app.core.config import AdminConfig
from app.exceptions.base import BaseAuthException
from app.providers import BaseProvider
from app.services.auth import AuthServiceABC


class AdminProvider(BaseProvider):
    def __init__(
        self,
        app: FastAPI,
        settings: AdminConfig,
        session_maker: async_sessionmaker[AsyncSession],
        auth_service: AuthServiceABC,
        httpx_client: AsyncClient,
    ):
        self.app = app
        self.auth_backend = AdminAuth(settings.secret_key, httpx_client, auth_service, settings)
        self.admin = Admin(
            app,
            base_url="/admin",
            session_maker=session_maker,  # type: ignore
            debug=settings.debug,
            authentication_backend=self.auth_backend,
        )

    async def startup(self):
        """FastAPI startup event"""
        self.admin.add_view(SubscriptionsAdminView)
        self.admin.add_view(PaymentsAdminView)
        self.admin.add_view(TariffsAdminView)

    async def shutdown(self):
        """FastAPI shutdown event"""
        ...


class AdminAuth(AuthenticationBackend):
    def __init__(
        self,
        secret_key: str,
        httpx_client: AsyncClient,
        auth_service: AuthServiceABC,
        config: AdminConfig,
    ) -> None:
        super().__init__(secret_key)
        self._httpx_client = httpx_client
        self._auth_service = auth_service
        self._config = config

    async def login(self, request: Request) -> bool:
        form = await request.form()

        try:
            access_token = await self._get_access_token(str(form["username"]), str(form["password"]))
            await self._validate_access_token(access_token)
        except BaseAuthException:
            return False

        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        await self._validate_access_token(token)

        return True

    async def _get_access_token(self, email: str, password: str) -> str:
        login_data = {
            "email": email,
            "password": password,
        }

        response = await self._httpx_client.post(self._config.login_url, data=login_data)

        if response.status_code != HTTPStatus.OK:
            raise BaseAuthException
        response_data = response.json()
        return response_data["access_token"]

    async def _validate_access_token(self, access_token: str) -> None:
        auth_data = await self._auth_service.validate_access_token(access_token)
        if not auth_data.is_superuser:
            raise BaseAuthException

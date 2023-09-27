from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.api.routers.admin import (
    PaymentsAdminView,
    SubscriptionsAdminView,
    TariffsAdminView,
)
from app.core.config import AdminConfig
from app.providers import BaseProvider


class AdminProvider(BaseProvider):
    def __init__(self, app: FastAPI, settings: AdminConfig, session_maker: async_sessionmaker[AsyncSession]):
        self.app = app
        self.admin = Admin(
            app,
            base_url="/admin",
            session_maker=session_maker,  # type: ignore
            debug=settings.debug,
        )

    async def startup(self):
        """FastAPI startup event"""
        self.admin.add_view(SubscriptionsAdminView)
        self.admin.add_view(PaymentsAdminView)
        self.admin.add_view(TariffsAdminView)

    async def shutdown(self):
        """FastAPI shutdown event"""
        ...

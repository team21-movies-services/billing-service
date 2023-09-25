from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.providers import BaseProvider


class SQLAlchemyProvider(BaseProvider):
    def __init__(
        self,
        app: FastAPI,
        async_dns: str,
        echo_log: bool = False,
    ):
        self.app = app
        self.async_dns = async_dns
        self.echo_log = echo_log
        self.async_engine = create_async_engine(
            self.async_dns,
            echo=self.echo_log,
            max_overflow=20,
            pool_size=10,
        )
        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
        )

    async def startup(self):
        """FastAPI startup event"""
        setattr(self.app.state, "async_engine", self.async_engine)
        setattr(self.app.state, "async_session_maker", self.async_session_maker)

    async def shutdown(self):
        """FastAPI shutdown event"""
        await self.async_engine.dispose()

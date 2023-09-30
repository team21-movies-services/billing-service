from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from worker.core.config import Settings

__all__ = ["AsyncSQLAlchemyProvider", "SQLAlchemyProvider"]


class AsyncSQLAlchemyProvider:
    def __init__(
        self,
        settings: Settings,
    ):
        self.async_dsn = settings.postgres.database_url
        self.echo_log = settings.postgres.echo_log
        self.async_engine = create_async_engine(
            self.async_dsn,
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

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


class SQLAlchemyProvider:
    def __init__(
        self,
        settings: Settings,
    ):
        self.dsn = settings.postgres.database_url
        self.echo_log = settings.postgres.echo_log
        self.engine = create_engine(
            self.dsn,
            echo=self.echo_log,
            max_overflow=20,
            pool_size=10,
        )
        self.session_maker = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=Session,
            autocommit=False,
            autoflush=False,
        )

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session: Session = self.session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

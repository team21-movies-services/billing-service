from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from worker.core.config import Settings

from . import DbClientABC

__all__ = ["SQLAlchemyDbClient"]


class SQLAlchemyDbClient(DbClientABC):
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

    def get_session(self) -> Session:
        return self.session_maker()

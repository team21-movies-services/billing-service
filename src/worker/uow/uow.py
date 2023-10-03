import traceback
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from worker.clients import DbClientABC
from worker.repository import SubscriptionRepository, UserPaymentsRepository

__all__ = ["UnitOfWorkABC", "SqlAlchemyUoW"]


class UnitOfWorkABC(ABC):
    def __init__(self):
        self.payment_repo: UserPaymentsRepository | None = None
        self.subscription_repo: SubscriptionRepository | None = None

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUoW(UnitOfWorkABC):
    def __init__(self, pg_client: DbClientABC):
        super().__init__()
        self.session_factory = pg_client
        self.session: Session | None = None

    def __enter__(self):
        self.session = self.session_factory.get_session()
        self.payment_repo = UserPaymentsRepository(self.session)
        self.subscription_repo = SubscriptionRepository(self.session)

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        if self.session:
            self.session.rollback()
            self.session.close()

    def commit(self):
        if self.session:
            self.session.commit()

    def rollback(self):
        if self.session:
            self.session.rollback()

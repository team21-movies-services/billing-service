import traceback
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from worker.clients import DbClientABC
from worker.repository import SubscriptionRepository, UserPaymentsRepository

__all__ = ["UnitOfWorkABC", "SqlAlchemyUoW"]


class UnitOfWorkABC(ABC):
    payment_repo: UserPaymentsRepository
    subscription_repo: SubscriptionRepository

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
    _session: Session

    def __init__(self, pg_client: DbClientABC):
        self.session_factory = pg_client

    def __enter__(self):
        self._session = self.session_factory.get_session()
        self.payment_repo = UserPaymentsRepository(self._session)
        self.subscription_repo = SubscriptionRepository(self._session)

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        self._session.rollback()
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

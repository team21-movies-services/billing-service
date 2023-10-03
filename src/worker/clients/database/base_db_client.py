from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

__all__ = ["DbClientABC"]


class DbClientABC(ABC):
    @abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError

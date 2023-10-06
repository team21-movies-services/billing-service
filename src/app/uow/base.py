from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWorkABC(ABC):
    @abstractmethod
    async def __aenter__(self) -> UnitOfWorkABC:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

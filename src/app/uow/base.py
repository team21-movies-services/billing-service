from abc import ABC, abstractmethod


class UnitOfWorkABC(ABC):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class IUnitOfWork:
    def __init__(self):
        ...

    def __aenter__(self):
        ...

    def __aexit__(self, *args):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

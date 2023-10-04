from abc import ABC, abstractmethod
from typing import Any


class BaseHttpClient(ABC):
    @abstractmethod
    def get(
        self,
        path: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def post(
        self,
        path: str,
        headers: dict | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        raise NotImplementedError

import logging
from typing import Any

import httpx
from httpx import codes
from shared.exceptions.clients import HTTPClientException

from .base import BaseHttpClient

logger = logging.getLogger(__name__)


class HttpxHttpClient(BaseHttpClient):
    def __init__(self, httpx_client: httpx.Client):
        self.httpx_client = httpx_client

    def _request(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        data: dict | None = None,
    ) -> Any:
        response = self.httpx_client.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
        )
        if response.status_code != codes.OK:
            raise HTTPClientException(f"Error sending request. detail={response.content!r}")
        return response.json()

    def get(
        self,
        path: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        return self._request(
            method="GET",
            url=path,
            headers=headers,
            params=params,
        )

    def post(
        self,
        path: str,
        headers: dict | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        return self._request(
            method="POST",
            url=path,
            headers=headers,
            data=data,
            params=params,
        )

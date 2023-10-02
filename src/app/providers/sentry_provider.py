import sentry_sdk
from fastapi import FastAPI

from app.providers import BaseProvider


class SentryProvider(BaseProvider):
    def __init__(
        self,
        app: FastAPI,
        dsn: str,
    ):
        self.app = app
        self._dsn = dsn

    async def startup(self):
        sentry_sdk.init(dsn=self._dsn, traces_sample_rate=1.0)

    async def shutdown(self):
        client = sentry_sdk.Hub.current.client
        if client:
            client.close(timeout=2.0)

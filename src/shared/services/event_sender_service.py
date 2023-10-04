from dataclasses import dataclass

from shared.clients import BaseHttpClient


@dataclass
class EventSenderService:
    _http_client: BaseHttpClient

    def send_event(self, url: str, data: dict | None = None, headers: dict | None = None, params: dict | None = None):
        self._http_client.post(path=url, data=data, headers=headers, params=params)

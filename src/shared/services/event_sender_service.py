from dataclasses import dataclass

from shared.clients.http import AsyncHTTPClientABC


@dataclass
class EventSenderService:
    _http_client: AsyncHTTPClientABC

    def send_event(self, url: str, data: dict = None, headers: dict = None, params: dict = None):  # type: ignore
        self._http_client.post(path=url, data=data, headers=headers, params=params)

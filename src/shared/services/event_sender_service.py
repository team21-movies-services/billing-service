from dataclasses import dataclass

from shared.clients import BaseHttpClient
from shared.constants import EventTypes
from worker.core.config import Settings


@dataclass
class EventSenderService:
    _http_client: BaseHttpClient
    _settings: Settings

    def send_event(
        self,
        event_type: EventTypes,
        data: dict | None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ):
        url = self._settings.event_service.event_service_url
        send_data = {
            'event_type': event_type,
            'event_data': data,
        }
        self._http_client.post(path=url, data=send_data, headers=headers, params=params)

from dataclasses import dataclass

from shared.clients import BaseHttpClient
from shared.constants import EventTypes


@dataclass
class EventSenderService:
    _http_client: BaseHttpClient
    _url: str = 'https://4178e455-13d6-4c19-aad9-32017ec7f721.mock.pstmn.io/actions'

    def send_event(
        self,
        event_type: EventTypes,
        data: dict | None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ):
        send_data = {
            'event_type': event_type,
            'event_data': data,
        }
        self._http_client.post(path=self._url, data=send_data, headers=headers, params=params)

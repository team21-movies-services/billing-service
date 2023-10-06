from pydantic import Field
from pydantic_settings import BaseSettings


# Настройки Event-сервиса
class EventServiceSettings(BaseSettings):
    event_service_url: str = Field(default='', alias='EVENT_SERVICE_URL')


class SharedSettings(BaseSettings):
    event_service: EventServiceSettings = EventServiceSettings()

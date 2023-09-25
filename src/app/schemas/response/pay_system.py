from uuid import UUID

from .base import BaseModelResponse


class PaySystemResponse(BaseModelResponse):
    id: UUID
    name: str
    alias: str
    currency_code: str
    json_data: dict

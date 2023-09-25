from datetime import datetime
from uuid import UUID

from .base import BaseModelResponse


class TariffResponse(BaseModelResponse):
    id: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    alias: str
    cost: float
    period: int
    period_unit: str
    json_sale: dict

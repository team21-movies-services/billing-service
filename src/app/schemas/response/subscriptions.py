from datetime import datetime
from uuid import UUID

from .base import BaseModelResponse
from .tariff import TariffResponse


class UserSubscriptionResponse(BaseModelResponse):
    id: UUID
    tariff: TariffResponse
    user_id: UUID
    period_start: datetime
    period_end: datetime
    renew: bool

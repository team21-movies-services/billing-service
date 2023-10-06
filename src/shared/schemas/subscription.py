from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubscriptionAddSchema(BaseModel):
    user_id: UUID
    tariff_id: UUID
    user_payment_id: UUID
    period_start: datetime
    period_end: datetime
    is_disabled: bool
    renew: bool

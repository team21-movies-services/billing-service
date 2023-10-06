from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubscriptionAddSchema(BaseModel):
    user_id: UUID
    tariff_id: UUID
    user_payment_id: UUID
    period_start: datetime
    period_end: datetime
    is_disabled: bool
    renew: bool


class SubscriptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tariff_id: UUID
    user_payment_id: UUID
    user_id: UUID
    period_start: datetime
    period_end: datetime
    is_disabled: bool
    renew: bool
    renew_try_count: int

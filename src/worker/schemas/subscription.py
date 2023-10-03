from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

__all__ = ["SubscriptionSchema"]


class SubscriptionSchema(BaseModel):
    id: UUID
    start_date: datetime
    expire_date: datetime
    payment_id: UUID

from uuid import UUID

from pydantic import BaseModel


class SubscriptionRequest(BaseModel):
    tariff_id: UUID

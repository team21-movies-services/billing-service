from uuid import UUID

from pydantic import BaseModel


class PaymentStatus(BaseModel):
    id: UUID
    name: str
    alias: str

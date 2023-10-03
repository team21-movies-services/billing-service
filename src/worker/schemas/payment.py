from uuid import UUID

from pydantic import BaseModel

__all__ = ["PaymentSchema"]


class PaymentSchema(BaseModel):
    id: UUID
    status: str
    system: str

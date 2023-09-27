from uuid import UUID

from pydantic import BaseModel


class PaymentSchema(BaseModel):
    id: UUID
    status: str
    system: str

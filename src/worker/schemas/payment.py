from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["UserPaymentCreatedSchema"]


class UserPaymentCreatedSchema(BaseModel):
    id: UUID | None
    pay_system_alias: str
    pay_status_alias: str
    user_id: UUID
    payment_id: UUID
    amount: int
    purpose: str
    json_sale: dict = Field(default={})

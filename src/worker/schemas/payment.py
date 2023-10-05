from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["UserPaymentCreatedSchema", "ErrorAction"]


class ErrorAction(StrEnum):
    set_inactive = "set_inactive"
    retry = "retry"


class UserPaymentCreatedSchema(BaseModel):
    id: UUID | None
    system_alias: str
    status_alias: str
    user_id: UUID
    payment_id: UUID
    error_action: ErrorAction | None = Field(default=None)
    amount: int
    purpose: str
    json_sale: dict = Field(default={})

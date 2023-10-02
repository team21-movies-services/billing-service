from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserPaymentAddSchema(BaseModel):
    user_id: UUID
    pay_system_id: UUID
    pay_status_id: UUID
    amount: str
    payment_id: Optional[UUID] = None
    purpose: Optional[str] = None

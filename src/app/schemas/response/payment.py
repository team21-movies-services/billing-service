from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .base import BaseModelResponse


class UserPaymentResponse(BaseModelResponse):
    id: UUID
    amount: Decimal
    pay_system: str
    currency_code: str
    pay_status: str
    purpose: str
    payment_id: str
    json_detail: dict
    created_at: datetime


class PaymentSchema(BaseModelResponse):
    id: UUID
    status: str
    system: str

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from shared.database.models.tariff import TariffPeriodUnit


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class PayStatusDTO(BaseDTO):
    id: UUID
    name: str
    alias: str
    created_at: datetime | None
    updated_at: datetime | None


class TariffDTO(BaseDTO):
    id: UUID
    name: str
    alias: str
    cost: int
    period: int
    period_unit: TariffPeriodUnit

    def info(self):
        match self.period_unit:
            case TariffPeriodUnit.day:
                ru_period_unit = "день"
            case TariffPeriodUnit.month:
                ru_period_unit = "месяц"
            case TariffPeriodUnit.year:
                ru_period_unit = "год"
            case _:
                ru_period_unit = self.period_unit
        return f"{self.name}, Срок: {self.period} {ru_period_unit}"


class PaySystemDTO(BaseDTO):
    id: UUID
    name: str
    alias: str


class UserPaymentDTO(BaseDTO):
    id: UUID
    pay_system: PaySystemDTO
    pay_status: PayStatusDTO
    user_id: UUID
    pay_system_id: UUID
    pay_status_id: UUID
    payment_id: UUID
    amount: int
    purpose: str
    json_sale: dict = Field(default={})


class UserSubscriptionDTO(BaseDTO):
    id: UUID
    tariff_id: UUID
    user_id: UUID
    tariff: TariffDTO
    period_start: datetime
    period_end: datetime
    user_payment: UserPaymentDTO
    is_disabled: bool
    renew: bool
    renew_try_count: int
    last_check: datetime | None

    def get_yookassa_payment_json(self) -> dict:
        payment = {
            "amount": {
                "value": self.tariff.cost,
                "currency": "RUB",
            },
            "capture": True,
            "description": f"Оплата подписки: {self.tariff.info()}",
        }
        if self.user_payment.payment_id:
            payment["payment_method_id"] = self.user_payment.payment_id
        return payment

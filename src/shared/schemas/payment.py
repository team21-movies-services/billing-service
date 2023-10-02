from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel


class PaymentSchema(BaseModel):
    id: UUID
    status: str
    system: str


class PaymentResponseSchema(BaseModel):
    id: str
    status: str
    redirect_url: str


class PaymentMethodEnum(StrEnum):
    bank_card = auto()


class ConfirmationTypeEnum(StrEnum):
    redirect = auto()


class PaymentAmount(BaseModel):
    value: str
    currency: str


class PaymentMethod(BaseModel):
    type: str = PaymentMethodEnum.bank_card.value


class PaymentConfirmation(BaseModel):
    type: str = ConfirmationTypeEnum.redirect.value
    return_url: str


class PaymentAddSchema(BaseModel):
    description: str
    amount: PaymentAmount
    confirmation: PaymentConfirmation
    payment_method_data: PaymentMethod = PaymentMethod()

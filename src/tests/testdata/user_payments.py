import datetime
import uuid
from typing import Literal, NotRequired, TypedDict

import pytest
from mimesis import Field, Locale, Schema
from shared.database.models import UserPayment

purposes = ["subscription"]


class UserPaymentParams(TypedDict):
    id: NotRequired[uuid.UUID]
    user_id: NotRequired[uuid.UUID]
    pay_system_id: NotRequired[uuid.UUID]
    amount: NotRequired[int]
    json_sale: NotRequired[dict]
    purpose: NotRequired[Literal["subscription"]]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]
    value: int | float


@pytest.fixture()
def get_user_payments(
    faker_seed,
):
    def factory(obj_quantity: int, **fields: UserPaymentParams) -> list[UserPayment]:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            iterations=obj_quantity,
            schema=lambda: {
                "id": uuid.uuid4(),
                "user_id": uuid.uuid4(),
                "pay_system_id": uuid.uuid4(),
                "payment_id": uuid.uuid4(),
                "amount": mf("age", maximum=99, minimum=1),
                "json_sale": {},
                "purpose": mf("choice", items=purposes),
                "created_at": mf("datetime.date"),
                "updated_at": mf("datetime.date"),
            },
        )
        results: list[dict] = schema.create()
        if fields:
            [result.update(fields) for result in results]
        return [UserPayment(**result) for result in results]  # type ignore: [misc]

    return factory

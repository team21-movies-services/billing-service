from shared.database.models.user_payment import UserPayment
from sqladmin import ModelView


class PaymentsAdminView(ModelView, model=UserPayment):  # type: ignore
    column_list = [
        UserPayment.id,
        UserPayment.user_id,
        UserPayment.amount,
        UserPayment.purpose,
        UserPayment.json_sale,
    ]

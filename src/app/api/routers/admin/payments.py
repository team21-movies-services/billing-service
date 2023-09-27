from shared.database.models.user_payment import UserPayment
from sqladmin import ModelView


class PaymentsAdminView(ModelView, model=UserPayment):  # type: ignore
    name_plural = "Платежи пользователей"

    column_list = [
        UserPayment.user_id,
        UserPayment.amount,
        UserPayment.purpose,
        UserPayment.pay_system,
        UserPayment.pay_status,
        UserPayment.json_sale,
    ]

    column_labels = {
        UserPayment.id: "ID записи",
        UserPayment.user_id: "ID пользователя",
        UserPayment.amount: "Сумма платежа",
        UserPayment.purpose: "Назначение платежа",
        UserPayment.json_sale: "Детали платежа",
        UserPayment.pay_system_id: "ID платежной системы",
        UserPayment.pay_status_id: "ID статуса платежа",
        UserPayment.payment_id: "ID платежа во внешней системе",
        UserPayment.updated_at: "Дата создания записи",
        UserPayment.created_at: "Дата обновления записи",
        UserPayment.pay_system: "Платежная система",
        UserPayment.pay_status: "Статус платежа",
    }

    can_create = False
    can_edit = False
    can_delete = False

from shared.database.models.user_subscription import UserSubscription
from sqladmin import ModelView


class SubscriptionsAdminView(ModelView, model=UserSubscription):  # type: ignore
    name_plural = "Подписки пользователей"

    column_list = [
        UserSubscription.user_id,
        UserSubscription.period_start,
        UserSubscription.period_end,
        UserSubscription.tariff,
    ]

    column_labels = {
        UserSubscription.id: "ID записи",
        UserSubscription.user_id: "ID пользователя",
        UserSubscription.period_start: "Старт подписки",
        UserSubscription.period_end: "Окончание подписки",
        UserSubscription.tariff: "Тариф",
        UserSubscription.tariff_id: "ID тарифа",
        UserSubscription.updated_at: "Дата создания записи",
        UserSubscription.created_at: "Дата обновления записи",
    }

    can_create = False
    can_edit = False
    can_delete = False

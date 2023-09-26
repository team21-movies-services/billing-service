from shared.database.models.user_subscription import UserSubscription
from sqladmin import ModelView


class SubscriptionsAdminView(ModelView, model=UserSubscription):  # type: ignore
    column_list = [
        UserSubscription.id,
        UserSubscription.user_id,
        UserSubscription.tariff_id,
        UserSubscription.period_start,
        UserSubscription.period_end,
    ]

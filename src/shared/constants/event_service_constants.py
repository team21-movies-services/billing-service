from enum import StrEnum


class EventTypes(StrEnum):
    succes_subscription = "Подписка оформлена"
    cancel_subscription = "Подписка отменена"
    renewal_subscription = "Подписка продлена"
    error_retry = "Ошибка при списании"

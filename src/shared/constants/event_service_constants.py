from enum import StrEnum


class EventTypes(StrEnum):
    SuccesSubscription = "Подписка оформлена"
    CancelSubscripton = "Подписка отменена"
    RenewalSubscription = "Подписка продлена"
    ErrorRetry = "Ошибка при списании"

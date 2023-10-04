import logging
from dataclasses import dataclass

from shared.database.dto import UserSubscriptionDTO
from worker.core.config import Settings
from worker.providers import ProviderFactory
from worker.uow import UnitOfWorkABC

logger = logging.getLogger(__name__)


@dataclass
class SubscriptionService:
    _provider_factory: ProviderFactory
    _settings: Settings
    _uow: UnitOfWorkABC

    def disable(self):
        with self._uow:
            subs = self._uow.subscription_repo.disable()
            self._uow.commit()
            # TODO: отправка события о деактивации подписки
            logger.info("Subscriptions with ids %s disabled.", ", ".join(str(sub.id) for sub in subs))
        logger.info("Subscriptions disable task complete")

    def make_recurrent_payment(self):
        logger.debug("make_recurrent_payment called")
        with self._uow:
            subs_gen = self._uow.subscription_repo.get_subscriptions_expires_in(days=0)
            for subs_pack in subs_gen:
                logger.debug(subs_pack)
                self._handle_pack_of_subscriptions(subs_pack)
                # TODO: обновить данные о платеже в бд
                self._uow.commit()
            return

    def _handle_pack_of_subscriptions(self, subscriptions: list[UserSubscriptionDTO]):
        for sub in subscriptions:
            self._handle_subscription(sub)

    def _handle_subscription(self, subscription: UserSubscriptionDTO):
        new_payment = self._uow.payment_repo.create_blank_payment(subscription)
        logger.debug(new_payment)
        provider = self._provider_factory.get_payment_provider(subscription.user_payment.pay_system.alias)
        payment_result = provider.make_recurrent_payment(subscription)
        if not payment_result:
            logger.error("Payment %s error", subscription)
            self._uow.subscription_repo.increment_subscription_retries(subscription)
            return
            # TODO: сделать что-то
            # TODO: обработать ошибку платежа и статус failed
        logger.info("Payment done %s", payment_result)

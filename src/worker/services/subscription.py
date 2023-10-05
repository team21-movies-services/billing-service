import logging
from dataclasses import dataclass

from shared.database.dto import UserSubscriptionDTO
from shared.exceptions import PaymentCancelledException, PaymentExternalApiException
from worker.core.config import Settings
from worker.providers import ProviderFactory
from worker.schemas import ErrorAction
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
            subs_gen = self._uow.subscription_repo.get_subscriptions_for_renew()
            for sub in subs_gen:
                logger.debug(sub)
                self._handle_subscription(sub)
            return

    def _handle_subscription(self, subscription: UserSubscriptionDTO):
        new_payment = self._uow.payment_repo.create_blank_payment(subscription)
        provider = self._provider_factory.get_payment_provider(subscription.user_payment.pay_system.alias)
        try:
            payment_result = provider.make_recurrent_payment(subscription)
            if payment_result.status_alias == "succeeded":
                self._uow.subscription_repo.update_end_period(subscription)
                self._uow.payment_repo.set_status(new_payment.id, payment_result.status_alias)
            # TODO: Отправить сообщение
            # TODO: Обнулить счетчик
        except PaymentExternalApiException:
            logger.warning("Error occurred while make recurrent payment for subscription %s", subscription.id)
            self._uow.subscription_repo.increment_retries(subscription)
            self._uow.payment_repo.set_status(new_payment.id, "failed")
        except PaymentCancelledException as e:
            self._handle_error_action(subscription, e.error_action)
        finally:
            self._uow.subscription_repo.update_last_checked(subscription)
            self._uow.commit()

    def _handle_error_action(self, subscription: UserSubscriptionDTO, payment_action: ErrorAction):
        match payment_action:
            case ErrorAction.retry:
                logger.error("Repeat later")
                self._uow.subscription_repo.increment_retries(subscription)
                # TODO: Send message about an error(or no)
            case ErrorAction.set_inactive:
                logger.error("SET INACTIVE")
                self._uow.subscription_repo.disable()
            case _:
                pass

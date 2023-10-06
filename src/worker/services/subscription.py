import logging
from dataclasses import dataclass

from shared.constants import EventTypes
from shared.database.dto import UserSubscriptionDTO
from shared.exceptions import PaymentCancelledException, PaymentExternalApiException
from shared.services import EventSenderService
from worker.core.config import Settings
from worker.providers import ProviderFactory
from worker.schemas import ErrorAction
from worker.schemas.status import StatusEnum
from worker.uow import UnitOfWorkABC

logger = logging.getLogger(__name__)


@dataclass
class SubscriptionService:
    _provider_factory: ProviderFactory
    _settings: Settings
    _uow: UnitOfWorkABC
    _event_service: EventSenderService

    def disable(self):
        with self._uow:
            subs = self._uow.subscription_repo.disable()
            self._uow.commit()
            # TODO: отправка события о деактивации подписки
            for sub in subs:
                cancel_event_data = {
                    "user_id": sub.user_id,
                    "sub_id": sub.id,
                    "tariff_id": sub.tariff_id,
                }
                self._event_service.send_event(event_type=EventTypes.CancelSubscripton, data=cancel_event_data)
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
            provider.make_recurrent_payment(subscription)
            self._uow.payment_repo.set_status(new_payment.id, status=StatusEnum.succeeded)
            self._uow.subscription_repo.update_end_period(subscription)
            self._uow.subscription_repo.increment_retries(subscription, reset=True)
            # TODO: Отправить сообщение что подписка продлена
        except PaymentExternalApiException as e:
            logger.warning("Error occurred while make recurrent payment for subscription %s", subscription.id)
            logger.error(e)
            self._uow.subscription_repo.increment_retries(subscription)
            self._uow.payment_repo.set_status(new_payment.id, StatusEnum.failed)
        except PaymentCancelledException as e:
            self._uow.payment_repo.set_status(new_payment.id, StatusEnum.canceled)
            self._handle_error_action(subscription, e.error_action)
        finally:
            self._uow.subscription_repo.update_last_checked(subscription)
            self._uow.commit()

    def _handle_error_action(self, subscription: UserSubscriptionDTO, payment_action: ErrorAction):
        match payment_action:
            case ErrorAction.retry:
                self._uow.subscription_repo.increment_retries(subscription)
                # TODO: Отправить сообщение что возникла ошибка при списании
            case ErrorAction.set_inactive:
                self._uow.subscription_repo.disable_one(subscription)
                # TODO: Отправить сообщение что подписка отменена
            case _:
                raise NotImplementedError

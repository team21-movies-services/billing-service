import logging
from dataclasses import dataclass
from uuid import UUID

from shared.constants import EventTypes
from shared.database.dto import UserSubscriptionDTO
from shared.exceptions import PaymentCancelledException, PaymentExternalApiException
from shared.providers.payments import ProviderFactory
from shared.schemas.payment import ErrorAction
from shared.schemas.status import StatusEnum
from shared.services import EventSenderService
from worker.core.config import Settings
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
            for sub in subs:
                self._send_disable_event(user_id=sub.user_id, sub_id=sub.id, tariff_id=sub.tariff_id)
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
            renewal_event_data = {
                "user_id": subscription.user_id,
                "tariff": subscription.tariff,
                "period_end": subscription.period_end,
                "user_payment": subscription.user_payment,
            }
            self._event_service.send_event(event_type=EventTypes.renewal_subscription, data=renewal_event_data)
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
                retry_error_data = {
                    "user_id": subscription.user_id,
                    "sub_id": subscription.id,
                }
                self._event_service.send_event(event_type=EventTypes.error_retry, data=retry_error_data)
            case ErrorAction.set_inactive:
                self._uow.subscription_repo.disable_one(subscription)
                self._send_disable_event(
                    user_id=subscription.user_id,
                    sub_id=subscription.id,
                    tariff_id=subscription.tariff_id,
                )
            case _:
                raise NotImplementedError

    def _send_disable_event(self, user_id: UUID, sub_id: UUID, tariff_id: str) -> None:
        disable_event_data = {
            "user_id": user_id,
            "sub_id": sub_id,
            "tariff_id": tariff_id,
        }
        self._event_service.send_event(event_type=EventTypes.cancel_subscription, data=disable_event_data)

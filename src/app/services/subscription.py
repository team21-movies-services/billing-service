import logging
from abc import ABC, abstractmethod
from uuid import UUID

from shared.exceptions.not_exist import (
    PayStatusDoesNotExist,
    PaySystemDoesNotExist,
    TariffDoesNotExist,
)
from shared.providers.payments.factory import ProviderFactory
from shared.schemas.payment import PaymentAddSchema, PaymentAmount, PaymentConfirmation

from app.schemas.request.payment import UserPaymentAddSchema
from app.schemas.response.subscriptions import UserSubscriptionResponse
from app.uow.subscription_uow import ISubscriptionUoW

logger = logging.getLogger(__name__)


class SubscriptionServiceABC(ABC):
    @abstractmethod
    async def buy(self, pay_system_alias: str, user_id: UUID, tariff_id: UUID) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        raise NotImplementedError


class SubscriptionService(SubscriptionServiceABC):
    def __init__(self, subscription_uow: ISubscriptionUoW, payment_factory: ProviderFactory):
        self._subscription_uow = subscription_uow
        self.payment_factory = payment_factory

    async def buy(self, pay_system_alias: str, user_id: UUID, tariff_id: UUID) -> str:
        async with self._subscription_uow:
            pay_system = await self._subscription_uow.pay_system_repository.get_by_alias(pay_system_alias)
            logger.info(f"Get pay_system '{pay_system}'")
            if not pay_system:
                raise PaySystemDoesNotExist

            tariff = await self._subscription_uow.tariff_repository.get_by_id(tariff_id)
            logger.info(f"Get tariff '{tariff}'")
            if not tariff:
                raise TariffDoesNotExist

            status = await self._subscription_uow.payment_status_repository.get_by_alias("pending")
            if not status:
                raise PayStatusDoesNotExist

            payment_add_schema = UserPaymentAddSchema(
                user_id=user_id,
                pay_system_id=pay_system.id,
                pay_status_id=status.id,
                amount=str(tariff.cost),
            )

            payment = await self._subscription_uow.payment_repository.add_payment(payment_add_schema)
            if not payment:
                # FIXME: error 500
                raise Exception

            payment_provider = self.payment_factory.get_payment_provider(provider_name=pay_system.alias)

            payment_amount = PaymentAmount(
                value=str(tariff.cost),
                currency=pay_system.currency_code,
            )
            payment_confirmation = PaymentConfirmation(
                return_url=payment_provider.get_return_url(),
            )
            # FIXME: add payment integer number
            purpose = f"Order No. {payment.id}"
            payment_add_schema = PaymentAddSchema(
                amount=payment_amount,
                confirmation=payment_confirmation,
                description=purpose,
            )

            payment_response = payment_provider.create_payment(payment_add_schema)
            if not payment_response:
                # FIXME: error 500
                raise Exception

            logger.info(f"\n\nPayment Response: Redirect url='{payment_response.redirect_url}'\n\n")

            upd_status = await self._subscription_uow.payment_status_repository.get_by_alias("waiting_for_capture")
            if not upd_status:
                raise PayStatusDoesNotExist

            payment = await self._subscription_uow.payment_repository.update_payment(
                payment_id=payment_response.id,
                status_id=upd_status.id,
            )

            await self._subscription_uow.commit()

        return payment_response.redirect_url

    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        async with self._subscription_uow:
            return await self._subscription_uow.subscription_repository.get_user_current_subscription(user_id)

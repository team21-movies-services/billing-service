import logging
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from shared.exceptions import (
    PaymentCreateError,
    PayStatusDoesNotExist,
    PaySystemDoesNotExist,
    SubscriptionCreateError,
    TariffDoesNotExist,
)
from shared.exceptions.clients import HTTPClientException
from shared.providers.payments.factory import ProviderFactory
from shared.schemas.payment import PaymentAddSchema, PaymentAmount, PaymentConfirmation
from shared.schemas.subscription import SubscriptionAddSchema

from app.schemas.request.payment import UserPaymentAddSchema
from app.schemas.response.subscriptions import UserSubscriptionResponse
from app.uow.subscription_uow import ISubscriptionUoW

logger = logging.getLogger(__name__)


class SubscriptionServiceABC(ABC):
    @abstractmethod
    async def buy(self, pay_system_alias: str, user_id: UUID, tariff_id: UUID, renew: bool) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        raise NotImplementedError

    @abstractmethod
    async def cancel(self, user_id: UUID) -> None:
        raise NotImplementedError


class SubscriptionService(SubscriptionServiceABC):
    def __init__(self, subscription_uow: ISubscriptionUoW, payment_factory: ProviderFactory):
        self._subscription_uow = subscription_uow
        self.payment_factory = payment_factory

    async def _get_pay_system(self, pay_system_alias: str):
        pay_system = await self._subscription_uow.pay_system_repository.get_by_alias(pay_system_alias)
        logger.info(f"Get pay_system '{pay_system}'")
        if not pay_system:
            raise PaySystemDoesNotExist
        return pay_system

    async def _get_tariff(self, tariff_id: UUID):
        tariff = await self._subscription_uow.tariff_repository.get_by_id(tariff_id)
        logger.info(f"Get tariff '{tariff}'")
        if not tariff:
            raise TariffDoesNotExist
        return tariff

    async def _get_payment_status(self, payment_status: str):
        status = await self._subscription_uow.payment_status_repository.get_by_alias(payment_status)
        if not status:
            raise PayStatusDoesNotExist
        return status

    async def _create_payment(self, user_id: UUID, pay_system_id: UUID, status_id: UUID, amount: str):
        payment_add_schema = UserPaymentAddSchema(
            user_id=user_id,
            pay_system_id=pay_system_id,
            pay_status_id=status_id,
            amount=amount,
        )
        payment = await self._subscription_uow.payment_repository.add_payment(payment_add_schema)
        if not payment:
            raise PaymentCreateError

        return payment

    async def _update_payment(self, payment_id: UUID, external_payment_id: str):
        status = await self._get_payment_status("pending")
        await self._subscription_uow.payment_repository.update_payment(
            id=payment_id,
            payment_id=external_payment_id,
            status_id=status.id,
        )

    async def _create_external_payment(self, pay_system_alias: str, payment_id: UUID, currency_code: str, amount: str):
        payment_provider = self.payment_factory.get_payment_provider(provider_name=pay_system_alias)

        payment_amount = PaymentAmount(
            value=amount,
            currency=currency_code,
        )
        payment_confirmation = PaymentConfirmation(
            return_url=payment_provider.get_return_url(),
        )
        # FIXME: add payment integer number
        purpose = f"Order No. {payment_id}"
        payment_add_schema = PaymentAddSchema(
            amount=payment_amount,
            confirmation=payment_confirmation,
            description=purpose,
        )

        payment_response = payment_provider.create_payment(payment_add_schema)
        if not payment_response:
            raise HTTPClientException

        logger.info(f"\nPayment Response: Payment Id: {payment_response.id}")
        logger.info(f"\n\nPayment Response: Redirect url='{payment_response.redirect_url}'\n\n")

        return payment_response

    async def _create_user_subscription(
        self,
        user_id: UUID,
        tariff_id: UUID,
        payment_id: UUID,
        renew: bool,
    ):
        period_start = datetime.utcnow()
        period_end = datetime.utcnow()
        subscription_add = SubscriptionAddSchema(
            user_id=user_id,
            tariff_id=tariff_id,
            user_payment_id=payment_id,
            is_disabled=True,
            period_start=period_start,
            period_end=period_end,
            renew=renew,
        )
        subscription = await self._subscription_uow.subscription_repository.add_subscription(subscription_add)
        if not subscription:
            raise SubscriptionCreateError

    async def buy(self, pay_system_alias: str, user_id: UUID, tariff_id: UUID, renew: bool) -> str:
        """
        Метод покупки пользователем подписки

        Raises:
            PaySystemDoesNotExist
            TariffDoesNotExist
            PayStatusDoesNotExist
            PaymentCreateError
            SubscriptionCreateError
            HTTPClientException
        """
        async with self._subscription_uow:
            pay_system = await self._get_pay_system(pay_system_alias)
            tariff = await self._get_tariff(tariff_id)
            status = await self._get_payment_status("created")

            tariff_cost = str(tariff.cost)
            payment = await self._create_payment(user_id, pay_system.id, status.id, tariff_cost)

            payment_response = await self._create_external_payment(
                pay_system_alias=pay_system.alias,
                payment_id=payment.id,
                amount=tariff_cost,
                currency_code=pay_system.currency_code,
            )

            await self._update_payment(payment.id, payment_response.id)
            await self._create_user_subscription(user_id, tariff.id, payment.id, renew)

            await self._subscription_uow.commit()

        return payment_response.redirect_url

    async def get_user_current_subscription(self, user_id: UUID) -> UserSubscriptionResponse:
        async with self._subscription_uow:
            return await self._subscription_uow.subscription_repository.get_user_current_subscription(user_id)

    async def cancel(self, user_id: UUID) -> None:
        async with self._subscription_uow:
            return await self._subscription_uow.subscription_repository.cancel_renew_by_user_id(user_id)

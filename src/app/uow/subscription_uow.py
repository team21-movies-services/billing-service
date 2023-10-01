from __future__ import annotations

from app.repositories.pay_system import PaySystemRepository, PaySystemRepositoryABC
from app.repositories.payment import PaymentRepository, PaymentRepositoryABC
from app.repositories.tariff import TariffRepository, TariffRepositoryABC
from app.repositories.user_subscription import (
    UserSubscriptionRepository,
    UserSubscriptionRepositoryABC,
)
from app.uow.base import UnitOfWorkABC


class ISubscriptionUoW(UnitOfWorkABC):
    tariff_repository: TariffRepositoryABC
    subscription_repository: UserSubscriptionRepositoryABC
    payment_repository: PaymentRepositoryABC
    pay_system_repository: PaySystemRepositoryABC


class SubscriptionUoW(ISubscriptionUoW):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self) -> SubscriptionUoW:
        self.session = self.session_factory()

        self.tariff_repository = TariffRepository(self.session)
        self.subscription_repository = UserSubscriptionRepository(self.session)
        self.payment_repository = PaymentRepository(self.session)
        self.pay_system_repository = PaySystemRepository(self.session)

        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

import pytest_asyncio
from shared.database.models.pay_status import PayStatus
from shared.database.models.pay_system import PaySystem
from shared.database.models.tariff import Tariff
from shared.database.models.user_payment import UserPayment
from sqlalchemy.ext.asyncio import AsyncSession
from tests.app.functional.testdata.pay_status import fake_pay_status
from tests.app.functional.testdata.pay_systems import fake_pay_system
from tests.app.functional.testdata.payments import fake_user_payment
from tests.app.functional.testdata.subscriptions import (
    fake_renew_subscription,
    fake_subscription,
)
from tests.app.functional.testdata.tariffs import fake_tariff

from app.schemas.domain.auth import AuthData


@pytest_asyncio.fixture()
async def tariffs(db_session: AsyncSession):
    _tariffs = [fake_tariff() for _ in range(5)]
    db_session.add_all(_tariffs)
    await db_session.commit()
    yield _tariffs
    for tariff in _tariffs:
        await db_session.delete(tariff)


@pytest_asyncio.fixture()
async def tariff(db_session: AsyncSession):
    tariff = fake_tariff()

    db_session.add(tariff)
    await db_session.commit()

    yield tariff

    await db_session.delete(tariff)


@pytest_asyncio.fixture()
async def pay_system(db_session: AsyncSession):
    pay_system = fake_pay_system()

    db_session.add(pay_system)
    await db_session.commit()

    yield pay_system

    await db_session.delete(pay_system)


@pytest_asyncio.fixture()
async def pay_status(db_session: AsyncSession):
    pay_status = fake_pay_status()

    db_session.add(pay_status)
    await db_session.commit()

    yield pay_status

    await db_session.delete(pay_status)


@pytest_asyncio.fixture()
async def user_payment(db_session: AsyncSession, auth_user: AuthData, pay_system: PaySystem, pay_status: PayStatus):
    user_payment = fake_user_payment(pay_system.id, pay_status.id, auth_user.user_id)

    db_session.add(user_payment)
    await db_session.commit()

    yield user_payment

    await db_session.delete(user_payment)


@pytest_asyncio.fixture()
async def subscription(db_session: AsyncSession, auth_user: AuthData, tariff: Tariff, user_payment: UserPayment):
    subscription = fake_subscription(tariff.id, user_payment.id, auth_user.user_id)

    db_session.add(subscription)
    await db_session.commit()

    yield subscription

    await db_session.delete(subscription)


@pytest_asyncio.fixture()
async def renew_subscription(db_session: AsyncSession, auth_user: AuthData, tariff: Tariff, user_payment: UserPayment):
    subscription = fake_renew_subscription(tariff.id, user_payment.id, auth_user.user_id)

    db_session.add(subscription)
    await db_session.commit()

    yield subscription

    await db_session.delete(subscription)

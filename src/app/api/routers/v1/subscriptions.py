import logging

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_auth_data
from app.schemas.domain.auth import AuthData
from app.schemas.request.subscriptions import SubscriptionRequest
from app.services.subscription import SubscriptionServiceABC

router = APIRouter(prefix='/subscriptions', tags=['Subscriptions'])

logger = logging.getLogger().getChild('subscriptions-router')


@router.post(
    '/{pay_system}/buy',
    summary="Оплата подписки пользователя",
    status_code=status.HTTP_200_OK,
)
async def _subscription_buy(
    pay_system: str,
    subscription_request: SubscriptionRequest,
    subscription_service: SubscriptionServiceABC = Depends(),
    auth_data: AuthData = Depends(get_auth_data),
):
    return await subscription_service.buy(
        pay_system_alias=pay_system,
        user_id=auth_data.user_id,
        tariff_id=subscription_request.tariff_id,
    )


@router.get(
    '/profile',
    summary="Текущая подписка пользователя",
    status_code=status.HTTP_200_OK,
)
async def _user_current_subscription(
    subscription_service: SubscriptionServiceABC = Depends(),
    auth_data: AuthData = Depends(get_auth_data),
):
    return await subscription_service.get_user_current_subscription(user_id=auth_data.user_id)

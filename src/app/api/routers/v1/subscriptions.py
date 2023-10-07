import logging

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_auth_data
from app.schemas.domain.auth import AuthData
from app.schemas.request.subscriptions import SubscriptionRequest
from app.schemas.response.subscriptions import UserSubscriptionResponse
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
    redirect_url = await subscription_service.buy(
        pay_system_alias=pay_system,
        user_id=auth_data.user_id,
        tariff_id=subscription_request.tariff_id,
        renew=subscription_request.renew,
    )
    return {"redirect_url": redirect_url}
    # return RedirectResponse(redirect_url, status_code=302)


@router.get(
    '/profile',
    summary="Текущая подписка пользователя",
    status_code=status.HTTP_200_OK,
    response_model=UserSubscriptionResponse,
)
async def _user_current_subscription(
    subscription_service: SubscriptionServiceABC = Depends(),
    auth_data: AuthData = Depends(get_auth_data),
):
    return await subscription_service.get_user_current_subscription(user_id=auth_data.user_id)


@router.post(
    '/cancel',
    summary="Отмена автопродления подписки",
    status_code=status.HTTP_200_OK,
)
async def _subscription_cancel(
    subscription_service: SubscriptionServiceABC = Depends(),
    auth_data: AuthData = Depends(get_auth_data),
):
    return await subscription_service.cancel(user_id=auth_data.user_id)

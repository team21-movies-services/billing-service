from http import HTTPStatus

import pytest
from httpx import AsyncClient
from shared.database.models.user_subscription import UserSubscription

from app.schemas.domain.auth import AuthData


@pytest.mark.parametrize(
    ("method", "route", "expected_status"),
    [("POST", "/api/v1/subscriptions/cancel", HTTPStatus.OK)],
)
async def test_cancel_subscription(
    api_client: AsyncClient,
    method: str,
    route: str,
    expected_status: int,
    renew_subscription: UserSubscription,
    auth_user: AuthData,
):
    assert renew_subscription.renew is True

    response = await api_client.request(method=method, url=route)

    assert response.status_code == expected_status
    assert renew_subscription.id == renew_subscription.id
    assert renew_subscription.user_id == auth_user.user_id
    assert renew_subscription.renew is False


@pytest.mark.parametrize(
    ("method", "route", "expected_status"),
    [("POST", "/api/v1/subscriptions/cancel", HTTPStatus.FORBIDDEN)],
)
async def test_cancel_without_auth(
    api_client: AsyncClient, method: str, route: str, expected_status: int, access_token: str
):
    _ = access_token

    response = await api_client.request(method=method, url=route)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("method", "route", "header", "expected_status"),
    [("POST", "/api/v1/subscriptions/cancel", "Authorization", HTTPStatus.UNAUTHORIZED)],
)
async def test_cancel_with_bad_token(
    api_client: AsyncClient, method: str, route: str, header: str, expected_status: int, forbidden_access_token: str
):
    response = await api_client.request(method=method, url=route, headers={header: forbidden_access_token})

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("method", "route", "header", "expected_status"),
    [("POST", "/api/v1/subscriptions/cancel", "Authorization", HTTPStatus.UNAUTHORIZED)],
)
async def test_cancel_with_expire_token(
    api_client: AsyncClient, method: str, route: str, header: str, expected_status: int, expire_access_token: str
):
    response = await api_client.request(method=method, url=route, headers={header: expire_access_token})

    assert response.status_code == expected_status

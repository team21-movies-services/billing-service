from http import HTTPStatus

import pytest
from httpx import AsyncClient
from shared.database.models.user_subscription import UserSubscription

from app.schemas.domain.auth import AuthData


@pytest.mark.parametrize(
    ("method", "route", "expected_status"),
    [("GET", "/api/v1/subscriptions/profile", HTTPStatus.OK)],
)
async def test_get_profile(
    api_client: AsyncClient,
    method: str,
    route: str,
    expected_status: int,
    subscription: UserSubscription,
    auth_user: AuthData,
):
    response = await api_client.request(method=method, url=route)
    answer = response.json()

    assert response.status_code == expected_status
    assert len(answer) == 6
    assert answer["id"] == str(subscription.id)
    assert answer["user_id"] == str(auth_user.user_id)
    assert answer["tariff"]
    assert answer["period_start"]
    assert answer["period_end"]


@pytest.mark.parametrize(
    ("method", "route", "expected_status"),
    [("GET", "/api/v1/subscriptions/profile", HTTPStatus.NOT_FOUND)],
)
async def test_get_profile_not_found(api_client: AsyncClient, method: str, route: str, expected_status: int):
    response = await api_client.request(method=method, url=route)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("method", "route", "expected_status"),
    [("GET", "/api/v1/subscriptions/profile", HTTPStatus.FORBIDDEN)],
)
async def test_get_profile_without_auth(
    api_client: AsyncClient, method: str, route: str, expected_status: int, access_token: str
):
    _ = access_token

    response = await api_client.request(method=method, url=route)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("method", "route", "header", "expected_status"),
    [("GET", "/api/v1/subscriptions/profile", "Authorization", HTTPStatus.UNAUTHORIZED)],
)
async def test_get_profile_with_bad_token(
    api_client: AsyncClient,
    method: str,
    route: str,
    header: str,
    expected_status: int,
    forbidden_access_token: str,
):
    response = await api_client.request(method=method, url=route, headers={header: forbidden_access_token})

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("method", "route", "header", "expected_status"),
    [("GET", "/api/v1/subscriptions/profile", "Authorization", HTTPStatus.UNAUTHORIZED)],
)
async def test_get_profile_with_expire_token(
    api_client: AsyncClient, method: str, route: str, header: str, expected_status: int, expire_access_token: str
):
    response = await api_client.request(method=method, url=route, headers={header: expire_access_token})

    assert response.status_code == expected_status

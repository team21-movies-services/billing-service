from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    ("method", "route", "params", "json", "expected_status"),
    [("POST", "/api/v1/status", None, None, HTTPStatus.OK), ("GET", "/api/v1/pay-systems", None, None, HTTPStatus.OK)],
)
async def test_status(api_client, method, route, params, expected_status, json):
    """
    Минимальный тест который помогает проверить что приложение не падает при попытке обратиться на эндпоинт,
    легко добавить еще один параметр даже до того его писать чтобы было удобно проверять.
    Большие запросы лучше убрать в переменные где-нибудь над тестом для читаемости
    """
    response = await api_client.request(method=method, url=route, json=json, params=params)
    assert response.status_code == expected_status

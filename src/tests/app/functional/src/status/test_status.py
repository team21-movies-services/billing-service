from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    ("method", "route", "params", "json", "expected_status"),
    [("POST", "/api/v1/status", None, None, HTTPStatus.OK), ("GET", "/api/v1/pay-systems", None, None, HTTPStatus.OK)],
)
async def test_status(api_client, method, route, params, expected_status, json):
    response = await api_client.request(method=method, url=route, json=json)
    assert response.status_code == expected_status

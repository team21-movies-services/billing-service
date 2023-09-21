from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    ("route", "params", "json", "expected_status"),
    [
        ("/api/v1/status", None, None, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio()
async def test_status(api_client, route, params, expected_status, json):
    response = await api_client.post(route, json=json)
    assert response.status_code == expected_status

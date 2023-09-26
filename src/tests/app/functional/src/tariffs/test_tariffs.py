from http import HTTPStatus

import pytest
from httpx import AsyncClient
from shared.database.models import Tariff


@pytest.mark.skip(reason="Migration affects test")
@pytest.mark.parametrize(
    ("method", "route", "expected_status"),
    [("GET", "/api/v1/tariffs", HTTPStatus.OK)],
)
async def test_get_tariffs(api_client: AsyncClient, method, route, expected_status, tariffs: list[Tariff]):
    tariffs.sort(key=lambda tariff: tariff.cost)
    response = await api_client.request(method=method, url=route)
    results = response.json()

    assert response.status_code == expected_status
    assert len(results) == len(tariffs)
    for idx, result in enumerate(results):
        assert result["id"] == tariffs[idx].id
        assert result["created_at"] == tariffs[idx].created_at
        assert result["updated_at"] == tariffs[idx].updated_at
        assert result["name"] == tariffs[idx].name
        assert result["alias"] == tariffs[idx].alias
        assert result["cost"] == tariffs[idx].cost
        assert result["period"] == tariffs[idx].period
        assert result["period_unit"] == tariffs[idx].period_unit
        assert result["json_sale"] == tariffs[idx].json_sale

import logging

from fastapi import APIRouter, Depends, status

from app.schemas.response.tariff import TariffResponse
from app.services.tariff import TariffServiceABC

router = APIRouter(prefix='/tariffs', tags=['Tariffs'])

logger = logging.getLogger().getChild('tariffs-router')


@router.get(
    '',
    summary="Список тарифов",
    response_model=list[TariffResponse],
    status_code=status.HTTP_200_OK,
)
async def _get_tariffs(tariff_service: TariffServiceABC = Depends()) -> list[TariffResponse]:
    logger.debug('Get pay systems list')
    return await tariff_service.get_all()

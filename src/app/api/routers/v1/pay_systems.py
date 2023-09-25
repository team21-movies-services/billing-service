import logging

from fastapi import APIRouter, Depends, status

from schemas.response.pay_system import PaySystemResponse
from services.pay_system import PaySystemServiceABC

router = APIRouter(prefix='/pay-systems', tags=['Pay Systems'])

logger = logging.getLogger().getChild('pay-system-router')


@router.get(
    '',
    summary="Список поддерживаемых систем для оплаты",
    response_model=list[PaySystemResponse],
    status_code=status.HTTP_200_OK,
)
async def _get_pay_systems(pay_systems_service: PaySystemServiceABC = Depends()) -> list[PaySystemResponse]:
    logger.debug('Get pay systems list')
    return await pay_systems_service.get_pay_systems_list()

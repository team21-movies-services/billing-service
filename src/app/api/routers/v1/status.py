import logging

from fastapi import APIRouter, Depends, status

from app.schemas.response.status import StatusResponse
from app.services.status import StatusServiceABC

router = APIRouter(prefix='/status', tags=['Status'])

logger = logging.getLogger().getChild('status-router')


@router.post(
    '',
    summary="Получить статус API",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
)
async def _get_api_status(role_service: StatusServiceABC = Depends()) -> StatusResponse:
    logger.debug('Get api status')
    return await role_service.get_api_status()


@router.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

    return division_by_zero

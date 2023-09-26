import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_auth_data
from app.schemas.domain.auth import AuthData
from app.schemas.request.pagination import Pagination
from app.schemas.response.payment import UserPaymentResponse
from app.services.payment import PaymentServiceABC

router = APIRouter(prefix='/payments', tags=['Payments'])

logger = logging.getLogger().getChild('pay-system-router')


PaginationDep = Annotated[Pagination, Depends(Pagination)]


@router.get(
    '/profile',
    summary="История пользовательских платежей",
    response_model=list[UserPaymentResponse],
    status_code=status.HTTP_200_OK,
)
async def _get_user_payments(
    pagination: PaginationDep,
    payment_service: PaymentServiceABC = Depends(),
    auth_data: AuthData = Depends(get_auth_data),
) -> list[UserPaymentResponse]:
    logger.debug('Get payments for user with %s id', auth_data.user_id)
    return await payment_service.get_all_by_user_id(auth_data.user_id, pagination)

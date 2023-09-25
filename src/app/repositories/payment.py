from abc import ABC, abstractmethod
from uuid import UUID

from shared.database.models.user_payment import UserPayment
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import desc, select

from app.repositories.base import SQLAlchemyRepo
from app.schemas.request.pagination import PaymentsPagination
from app.schemas.response.payment import UserPaymentResponse


class PaymentRepositoryABC(ABC):
    @abstractmethod
    async def get_all_by_user_id(self, user_id: UUID, pagination: PaymentsPagination) -> list[UserPaymentResponse]:
        raise NotImplementedError


class PaymentRepository(SQLAlchemyRepo, PaymentRepositoryABC):
    async def get_all_by_user_id(self, user_id: UUID, pagination: PaymentsPagination) -> list[UserPaymentResponse]:
        query = (
            select(UserPayment)
            .where(UserPayment.user_id == user_id)
            .join(UserPayment.pay_system)
            .join(UserPayment.pay_status)
            .options(contains_eager(UserPayment.pay_system), contains_eager(UserPayment.pay_status))
            .order_by(desc(UserPayment.created_at))
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        query_result = await self._session.execute(query)
        db_objs = query_result.scalars().all()

        return [
            UserPaymentResponse(
                id=db_obj.id,
                amount=db_obj.amount,
                pay_system=db_obj.pay_system.name,
                currency_code=db_obj.pay_system.currency_code,
                pay_status=db_obj.pay_status.name,
                purpose=db_obj.purpose,
                payment_id=db_obj.payment_id,
                json_sale=db_obj.json_sale,
                created_at=db_obj.created_at,
            )
            for db_obj in db_objs
        ]

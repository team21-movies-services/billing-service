from abc import ABC, abstractmethod
from uuid import UUID

from shared.database.models.user_payment import UserPayment
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import desc, insert, select, update

from app.repositories.base import SQLAlchemyRepo
from app.schemas.request.pagination import Pagination
from app.schemas.request.payment import UserPaymentAddSchema
from app.schemas.response.payment import UserPaymentResponse


class PaymentRepositoryABC(ABC):
    @abstractmethod
    async def get_all_by_user_id(self, user_id: UUID, pagination: Pagination) -> list[UserPaymentResponse]:
        raise NotImplementedError

    @abstractmethod
    async def add_payment(self, payment_add_schema: UserPaymentAddSchema) -> UserPaymentResponse | None:
        raise NotImplementedError

    @abstractmethod
    async def update_payment(
        self,
        id: UUID,
        payment_id: str,
        status_id: UUID,
        purpose: str,
    ) -> UserPaymentResponse | None:
        raise NotImplementedError


class PaymentRepository(SQLAlchemyRepo, PaymentRepositoryABC):
    async def get_all_by_user_id(self, user_id: UUID, pagination: Pagination) -> list[UserPaymentResponse]:
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
                json_detail=db_obj.json_detail,
                created_at=db_obj.created_at,
            )
            for db_obj in db_objs
        ]

    async def add_payment(self, payment_add_schema: UserPaymentAddSchema) -> UserPaymentResponse | None:
        stmt = insert(UserPayment).values(**payment_add_schema.model_dump()).returning(UserPayment)
        result = await self._session.execute(stmt)
        if user_payment := result.scalar():
            return user_payment
            # FIXME: return UserPaymentResponse
            return UserPaymentResponse(
                id=user_payment.id,
                amount=user_payment.amount,
                pay_system=user_payment.pay_system.name,
                currency_code=user_payment.pay_system.currency_code,
                pay_status=user_payment.pay_status.name,
                purpose=user_payment.purpose,
                payment_id=user_payment.payment_id,
                json_detail=user_payment.json_detail,
                created_at=user_payment.created_at,
            )
        return None

    async def update_payment(
        self,
        id: UUID,
        payment_id: str,
        status_id: UUID,
        purpose: str,
    ) -> UserPaymentResponse | None:
        stmt = (
            update(UserPayment)
            .values(payment_id=payment_id, pay_status_id=status_id, purpose=purpose)
            .where(UserPayment.id == id)
            .returning(UserPayment)
        )
        result = await self._session.execute(stmt)
        if user_payment := result.scalar():
            return user_payment
        return None

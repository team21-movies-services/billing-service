import uuid

from sqlalchemy import PrimaryKeyConstraint, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column, RestrictForeignKey
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from models.pay_system import PaySystem
from models.pay_status import PayStatus


class UserPayment(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.user_payments db table."""

    __tablename__ = "user_payments"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_payment_pkey'),
    )

    pay_system_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(PaySystem.id),
        nullable=False,
        comment="ID платежной системы",
    )
    pay_status_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(PayStatus.id),
        nullable=False,
        comment="ID статуса платежа",
    )

    user_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        nullable=False,
        comment="ID пользователя",
    )
    payment_id: Mapped[str] = Column(Text, nullable=False, comment="ID платежа во внешней системе")
    amount: Mapped[str] = Column(Numeric(2), nullable=False, comment="Сумма платежа")
    purpose: Mapped[str] = Column(Text, nullable=False, comment="Назначение платежа")

    json_sale: Mapped[dict] = Column(
        JSONB,
        nullable=False,
        default={},
        server_default='{}',
        comment="Детали платежа (request/response)",
    )

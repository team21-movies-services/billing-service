import uuid

from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class PaySystem(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.pay_systems db table."""

    __tablename__ = "pay_systems"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pay_system_pkey'),
    )
    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        primary_key=True,
    )

    name: Mapped[str] = Column(String(127), nullable=False, comment="Название платёжной системы")
    alias: Mapped[str] = Column(String(127), nullable=False, comment="Алиас для обращения в коде")

    currency_code: Mapped[str] = Column(String(8), nullable=False, comment="Валюта по умолчанию")

    json_data: Mapped[dict] = Column(
        JSONB,
        nullable=False,
        default={},
        server_default='{}',
        comment="Доп. данные платежной системы",
    )

from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class PayStatus(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.pay_status db table."""

    __tablename__ = "pay_status"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pay_statu_pkey'),
    )

    name: Mapped[str] = Column(String(127), nullable=False, comment="Название платёжной системы")
    alias: Mapped[str] = Column(String(127), nullable=False, comment="Алиас для обращения в коде")

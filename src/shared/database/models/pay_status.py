from shared.database.models.base import BaseModel, Column
from shared.database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped


class PayStatus(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.pay_status db table."""

    __tablename__ = "pay_status"
    __table_args__ = (PrimaryKeyConstraint('id', name='pay_statu_pkey'),)

    name: Mapped[str] = Column(String(127), nullable=False, comment="Статус платежа")
    alias: Mapped[str] = Column(String(127), nullable=False, comment="Алиас для обращения в коде")

    def __repr__(self) -> str:
        return f"{self.name}"

import uuid
from datetime import datetime

from shared.database.models.base import BaseModel, Column, RestrictForeignKey
from shared.database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from shared.database.models.tariff import Tariff
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, relationship


class UserSubscription(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.user_subscriptions db table."""

    __tablename__ = "user_subscriptions"
    __table_args__ = (PrimaryKeyConstraint('id', name='user_subscriptions_pkey'),)

    tariff_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(Tariff.id),
        nullable=False,
        comment="ID тарифа",
    )
    user_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        nullable=False,
        comment="ID пользователя",
    )
    period_start: Mapped[datetime] = Column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=False,
        comment="Дата и время начала действия подписки",
    )
    period_end: Mapped[datetime] = Column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=False,
        comment="Дата и время окончания действия подписки",
    )

    tariff: Mapped[Tariff] = relationship()

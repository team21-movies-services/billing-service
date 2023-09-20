import uuid
from datetime import datetime

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column, RestrictForeignKey
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from models.tariff import Tariff


class UserSubscription(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.user_subscriptions db table."""

    __tablename__ = "user_subscriptions"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_subscriptions_pkey'),
    )

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

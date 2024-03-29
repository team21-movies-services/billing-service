import uuid
from datetime import datetime

from shared.database.models.base import BaseModel, Column, RestrictForeignKey
from shared.database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from shared.database.models.tariff import Tariff
from shared.database.models.user_payment import UserPayment
from sqlalchemy import BOOLEAN, INTEGER, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, relationship


class UserSubscription(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.user_subscriptions db table."""

    __tablename__ = "user_subscriptions"
    __table_args__ = (PrimaryKeyConstraint('id', name='user_subscriptions_pkey'),)

    tariff_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(Tariff.id, name='tariff_fkey'),
        nullable=False,
        comment="ID тарифа",
    )
    user_payment_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(UserPayment.id, name='user_payment_fkey'),
        nullable=True,
        comment="Связь с платежом пользователя",
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
    is_disabled: Mapped[bool] = Column(
        BOOLEAN,
        default=False,
        server_default="false",
        nullable=False,
        comment="Деактивирует подписку",
    )
    renew: Mapped[bool] = Column(
        BOOLEAN,
        default=False,
        server_default="false",
        nullable=False,
        comment="Вкл/Выкл автопродление подписки",
    )
    renew_try_count: Mapped[int] = Column(
        INTEGER,
        default=0,
        server_default="0",
        nullable=False,
        comment="Количество совершённых попыток автопродления платежа",
    )
    last_check: Mapped[datetime] = Column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=True,
        comment="Дата последней проверки подписки",
    )

    tariff: Mapped[Tariff] = relationship()
    user_payment: Mapped[UserPayment] = relationship()

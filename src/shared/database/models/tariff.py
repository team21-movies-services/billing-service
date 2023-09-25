from enum import StrEnum, auto

from shared.database.models.base import BaseModel, Column
from shared.database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from sqlalchemy import Integer, Numeric, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped


class TariffPeriodUnit(StrEnum):
    day = auto()
    month = auto()
    year = auto()


class Tariff(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.tariffs db table."""

    __tablename__ = "tariffs"
    __table_args__ = (PrimaryKeyConstraint('id', name='tariff_pkey'),)

    name: Mapped[str] = Column(String(127), nullable=False, comment="Название тарифа")
    alias: Mapped[str] = Column(String(127), nullable=False, comment="Алиас для обращения в коде")

    cost: Mapped[str] = Column(Numeric(2), nullable=False, comment="Цена тарифа")
    period: Mapped[int] = Column(Integer, nullable=False, comment="Период действия тарифа")

    period_unit: Mapped[str] = Column(
        ENUM(
            TariffPeriodUnit,
            name="tariff_period_unit",
            create_type=False,
            values_callable=lambda obj: obj._member_names_,
        ),
        nullable=True,
        comment="Единица измерения периода (месяц, день, год)",
    )

    json_sale: Mapped[dict] = Column(
        JSONB,
        nullable=False,
        default={},
        server_default='{}',
        comment="Скидки на тариф",
    )

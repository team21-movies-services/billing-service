"""add_tariff_and_pay_system

Revision ID: 04e65071a096
Revises: 1e06c683f268
Create Date: 2023-09-25 16:34:28.576113

"""
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '04e65071a096'
down_revision: Union[str, None] = '1e06c683f268'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.sql.text(
            f"""
            INSERT INTO tariffs (id, name, alias, cost, period, period_unit) VALUES
            (
                '{uuid4()}', 'Base', 'base', 5, 1, 'month'
            );
            """
        )
    )
    op.execute(
        sa.sql.text(
            f"""
            INSERT INTO pay_systems (id, name, alias, currency_code) VALUES
            (
                '{uuid4()}', 'ЮКасса', 'yookassa', 'RUB'
            );
            """
        )
    )


def downgrade() -> None:
    op.execute(sa.sql.text("DELETE FROM tariffs WHERE alias IN ('base')"))
    op.execute(sa.sql.text("DELETE FROM pay_systems WHERE alias IN ('yookassa')"))

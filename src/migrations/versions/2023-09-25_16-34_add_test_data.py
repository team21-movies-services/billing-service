"""add_tariff_and_pay_system

Revision ID: 04e65071a096
Revises: 1e06c683f268
Create Date: 2023-09-25 16:34:28.576113

"""
from typing import Sequence, Union
from uuid import UUID, uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '04e65071a096'
down_revision: Union[str, None] = '1e06c683f268'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    tariff_id = uuid4()
    op.execute(
        sa.sql.text(
            f"""
            INSERT INTO tariffs (id, name, alias, cost, period, period_unit) VALUES
            (
                '{tariff_id}', 'Base', 'base', 5, 1, 'month'
            );
            """
        )
    )
    pay_system_id = uuid4()
    op.execute(
        sa.sql.text(
            f"""
            INSERT INTO pay_systems (id, name, alias, currency_code) VALUES
            (
                '{pay_system_id}', 'ЮКасса', 'yookassa', 'RUB'
            );
            """
        )
    )
    pending_id = uuid4()
    waiting_for_capture_id = uuid4()
    succeeded_id = uuid4()
    canceled_id = uuid4()
    op.execute(
        sa.sql.text(
            f"""
            INSERT INTO pay_status (id, name, alias) VALUES
            ('{pending_id}', 'Платёж создан', 'pending'),
            ('{waiting_for_capture_id}', 'Ожидание списания', 'waiting_for_capture'),
            ('{succeeded_id}', 'Платеж успешно завершён', 'succeeded'),
            ('{canceled_id}', 'Платеж отменён', 'canceled');
            """
        )
    )
    user_id = UUID("7e3dad93-1401-4c7a-a401-1ee0f33d207e")
    op.execute(
        sa.sql.text(
            f"""
            INSERT INTO user_payments (id, pay_system_id, pay_status_id, user_id, payment_id, amount, purpose) VALUES
            ('{uuid4()}', '{pay_system_id}', '{succeeded_id}', '{user_id}', '{str(uuid4())}', '50', 'subscription'),
            ('{uuid4()}', '{pay_system_id}', '{succeeded_id}', '{user_id}', '{str(uuid4())}', '55', 'subscription'),
            ('{uuid4()}', '{pay_system_id}', '{succeeded_id}', '{user_id}', '{str(uuid4())}', '60', 'subscription'),
            ('{uuid4()}', '{pay_system_id}', '{canceled_id}', '{user_id}', '{str(uuid4())}', '65', 'subscription'),
            ('{uuid4()}', '{pay_system_id}', '{canceled_id}', '{user_id}', '{str(uuid4())}', '70', 'subscription');
            """
        )
    )


def downgrade() -> None:
    op.execute(sa.sql.text("DELETE FROM user_payments WHERE user_id IN ('7e3dad93-1401-4c7a-a401-1ee0f33d207e')"))
    op.execute(sa.sql.text("DELETE FROM tariffs WHERE alias IN ('base')"))
    op.execute(sa.sql.text("DELETE FROM pay_systems WHERE alias IN ('yookassa')"))
    op.execute(
        sa.sql.text("DELETE FROM pay_status WHERE alias IN ('pending', 'waiting_for_capture', 'succeeded', 'canceled')")
    )
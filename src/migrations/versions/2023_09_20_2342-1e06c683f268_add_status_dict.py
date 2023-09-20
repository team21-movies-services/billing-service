"""add_status_dict

Revision ID: 1e06c683f268
Revises: fe102f372c62
Create Date: 2023-09-20 23:42:48.573798

"""
from typing import Sequence, Union
from uuid import uuid4
import sqlalchemy as sa
from alembic import op
from sqlalchemy import orm


# revision identifiers, used by Alembic.
revision: str = '1e06c683f268'
down_revision: Union[str, None] = 'fe102f372c62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    db_bind = op.get_bind()
    session = orm.Session(bind=db_bind)
    session.execute(
        sa.sql.text(
            f"""
            INSERT INTO pay_status (id, name, alias) VALUES
            (
                '{uuid4()}', 'Успешная оплата', 'success'
            ),
            (
                '{uuid4()}', 'Ошибка оплаты', 'failed'
            ),
            (
                '{uuid4()}', 'Оплата отменена', 'canceled'
            );
            """
        )
    )


def downgrade() -> None:
    db_bind = op.get_bind()
    session = orm.Session(bind=db_bind)
    session.execute(sa.sql.text("DELETE FROM pay_status WHERE alias IN ('success', 'failed', 'canceled')"))
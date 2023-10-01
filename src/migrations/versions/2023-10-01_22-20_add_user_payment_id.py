"""add_user_payment_id

Revision ID: cd9807ed90b2
Revises: 04e65071a096
Create Date: 2023-10-01 22:20:14.854474

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cd9807ed90b2'
down_revision: Union[str, None] = '04e65071a096'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'pay_status',
        'name',
        existing_type=sa.VARCHAR(length=127),
        comment='Название платежной системы',
        existing_comment='Название платёжной системы',
        existing_nullable=False,
    )
    op.add_column(
        'user_subscriptions',
        sa.Column('user_payment_id', sa.UUID(), nullable=True, comment='Связь с платежом пользователя'),
    )
    op.create_foreign_key(
        'user_payment_fkey',
        'user_subscriptions',
        'user_payments',
        ['user_payment_id'],
        ['id'],
        onupdate='RESTRICT',
        ondelete='RESTRICT',
    )
    op.execute(
        sa.sql.text(
            f"""
                ALTER TABLE user_subscriptions ALTER COLUMN user_payment_id DROP NOT NULL;
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.sql.text(
            f"""
                ALTER TABLE user_subscriptions ALTER COLUMN user_payment_id DROP NOT NULL;
            """
        )
    )
    op.drop_constraint('user_payment_fkey', 'user_subscriptions', type_='foreignkey')
    op.drop_column('user_subscriptions', 'user_payment_id')
    op.alter_column(
        'pay_status',
        'name',
        existing_type=sa.VARCHAR(length=127),
        comment='Название платёжной системы',
        existing_comment='Название платежной системы',
        existing_nullable=False,
    )

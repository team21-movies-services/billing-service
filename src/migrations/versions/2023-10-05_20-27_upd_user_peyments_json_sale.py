"""upd_user_peyments_json_sale

Revision ID: c9138c25d377
Revises: 04e65071a096
Create Date: 2023-10-05 20:27:06.190664

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c9138c25d377'
down_revision: Union[str, None] = '04e65071a096'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'user_payments',
        sa.Column(
            'json_detail',
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{}',
            nullable=False,
            comment='Детали платежа (request/response)',
        ),
    )
    op.alter_column(
        'user_payments',
        'payment_id',
        existing_type=sa.TEXT(),
        nullable=True,
        existing_comment='ID платежа во внешней системе',
    )
    op.alter_column(
        'user_payments', 'purpose', existing_type=sa.TEXT(), nullable=True, existing_comment='Назначение платежа'
    )
    op.drop_column('user_payments', 'json_sale')
    op.alter_column(
        'user_subscriptions',
        'renew_try_count',
        existing_type=sa.INTEGER(),
        comment='Количество совершённых попыток автопродления платежа',
        existing_comment='Вкл/Выкл автопродление подписки',
        existing_nullable=False,
        existing_server_default=sa.text('0'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'user_subscriptions',
        'renew_try_count',
        existing_type=sa.INTEGER(),
        comment='Вкл/Выкл автопродление подписки',
        existing_comment='Количество совершённых попыток автопродления платежа',
        existing_nullable=False,
        existing_server_default=sa.text('0'),
    )
    op.add_column(
        'user_payments',
        sa.Column(
            'json_sale',
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            autoincrement=False,
            nullable=False,
            comment='Детали платежа (request/response)',
        ),
    )
    op.alter_column(
        'user_payments', 'purpose', existing_type=sa.TEXT(), nullable=False, existing_comment='Назначение платежа'
    )
    op.alter_column(
        'user_payments',
        'payment_id',
        existing_type=sa.TEXT(),
        nullable=False,
        existing_comment='ID платежа во внешней системе',
    )
    op.drop_column('user_payments', 'json_detail')
    # ### end Alembic commands ###

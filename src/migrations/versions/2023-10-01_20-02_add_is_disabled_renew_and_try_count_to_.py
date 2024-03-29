"""add is_disabled renew and try count to user_subscriptions

Revision ID: 158933409277
Revises: cd9807ed90b2
Create Date: 2023-10-01 20:02:57.957575

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '158933409277'
down_revision: Union[str, None] = '1e06c683f268'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'user_subscriptions',
        sa.Column('is_disabled', sa.BOOLEAN(), server_default='false', nullable=False, comment='Деактивирует подписку'),
    )
    op.add_column(
        'user_subscriptions',
        sa.Column(
            'renew', sa.BOOLEAN(), server_default='false', nullable=False, comment='Вкл/Выкл автопродление подписки'
        ),
    )
    op.add_column(
        'user_subscriptions',
        sa.Column(
            'renew_try_count',
            sa.INTEGER(),
            server_default='0',
            nullable=False,
            comment='Вкл/Выкл автопродление подписки',
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_subscriptions', 'renew_try_count')
    op.drop_column('user_subscriptions', 'renew')
    op.drop_column('user_subscriptions', 'is_disabled')
    # ### end Alembic commands ###

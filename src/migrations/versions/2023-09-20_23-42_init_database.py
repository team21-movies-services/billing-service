"""init_database

Revision ID: fe102f372c62
Revises: 
Create Date: 2023-09-20 23:42:41.242312

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fe102f372c62'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'pay_status',
        sa.Column('name', sa.String(length=127), nullable=False, comment='Название платёжной системы'),
        sa.Column('alias', sa.String(length=127), nullable=False, comment='Алиас для обращения в коде'),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pay_statu_pkey'),
    )
    op.create_table(
        'pay_systems',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=127), nullable=False, comment='Название платёжной системы'),
        sa.Column('alias', sa.String(length=127), nullable=False, comment='Алиас для обращения в коде'),
        sa.Column('currency_code', sa.String(length=8), nullable=False, comment='Валюта по умолчанию'),
        sa.Column(
            'json_data',
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{}',
            nullable=False,
            comment='Доп. данные платежной системы',
        ),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pay_system_pkey'),
    )
    op.create_table(
        'tariffs',
        sa.Column('name', sa.String(length=127), nullable=False, comment='Название тарифа'),
        sa.Column('alias', sa.String(length=127), nullable=False, comment='Алиас для обращения в коде'),
        sa.Column('cost', sa.Numeric(precision=2), nullable=False, comment='Цена тарифа'),
        sa.Column('period', sa.Integer(), nullable=False, comment='Период действия тарифа'),
        sa.Column(
            'period_unit',
            postgresql.ENUM('day', 'month', 'year', name='tariff_period_unit'),
            nullable=True,
            comment='Единица измерения периода (месяц, день, год)',
        ),
        sa.Column(
            'json_sale',
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{}',
            nullable=False,
            comment='Скидки на тариф',
        ),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='tariff_pkey'),
    )
    op.create_table(
        'user_payments',
        sa.Column('pay_system_id', sa.UUID(), nullable=False, comment='ID платежной системы'),
        sa.Column('pay_status_id', sa.UUID(), nullable=False, comment='ID статуса платежа'),
        sa.Column('user_id', sa.UUID(), nullable=False, comment='ID пользователя'),
        sa.Column('payment_id', sa.Text(), nullable=False, comment='ID платежа во внешней системе'),
        sa.Column('amount', sa.Numeric(precision=2), nullable=False, comment='Сумма платежа'),
        sa.Column('purpose', sa.Text(), nullable=False, comment='Назначение платежа'),
        sa.Column(
            'json_sale',
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{}',
            nullable=False,
            comment='Детали платежа (request/response)',
        ),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pay_status_id'], ['pay_status.id'], onupdate='RESTRICT', ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['pay_system_id'], ['pay_systems.id'], onupdate='RESTRICT', ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name='user_payment_pkey'),
    )
    op.create_table(
        'user_subscriptions',
        sa.Column('tariff_id', sa.UUID(), nullable=False, comment='ID тарифа'),
        sa.Column('user_id', sa.UUID(), nullable=False, comment='ID пользователя'),
        sa.Column(
            'period_start', postgresql.TIMESTAMP(), nullable=False, comment='Дата и время начала действия подписки'
        ),
        sa.Column(
            'period_end', postgresql.TIMESTAMP(), nullable=False, comment='Дата и время окончания действия подписки'
        ),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tariff_id'], ['tariffs.id'], onupdate='RESTRICT', ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name='user_subscriptions_pkey'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_subscriptions')
    op.drop_table('user_payments')
    op.drop_table('tariffs')
    op.drop_table('pay_systems')
    op.drop_table('pay_status')
    op.execute("DROP TYPE tariff_period_unit")
    # ### end Alembic commands ###

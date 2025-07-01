"""init

Revision ID: dd32bf85759a
Revises: 
Create Date: 2025-07-01 23:01:10.098275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd32bf85759a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('id', sa.INT(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_table('groups',
    sa.Column('id', sa.INT(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_groups')),
    sa.UniqueConstraint('name', name=op.f('uq_groups_name'))
    )
    op.create_table('messages',
    sa.Column('id', sa.INT(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('group_id', sa.INT(), nullable=False),
    sa.Column('user_id', sa.INT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    op.drop_table('groups')
    op.drop_table('messages')


"""Initial database structure

Revision ID: dfcc65b78d85
Revises: 
Create Date: 2024-12-23 09:52:47.139833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'dfcc65b78d85'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
    )
    
    op.create_table(
        'token_blacklist',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('token', sa.String(length=500), unique=True, nullable=False),
        sa.Column('blacklisted_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('token_blacklist')
    op.drop_table('users')

"""add teacher

Revision ID: 156ed0c60fd5
Revises: 0001_initial
Create Date: 2026-03-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '156ed0c60fd5'
down_revision: Union[str, Sequence[str], None] = '0001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'teachers',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('cpf', sa.String(), nullable=False, unique=True),
        sa.Column('telefone', sa.String(), nullable=True),
        sa.Column('genero', sa.String(), nullable=True),
        sa.Column('funcao', sa.String(), nullable=True),
        sa.Column('temporary', sa.Boolean(), default=False),
        sa.Column('outsource', sa.Boolean(), default=False),
        sa.Column('status', sa.Boolean(), default=True),
        sa.Column('data_ativacao', sa.Date(), nullable=True),
        sa.Column('data_desativacao', sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('teachers')
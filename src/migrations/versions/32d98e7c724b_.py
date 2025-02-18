"""empty message

Revision ID: 32d98e7c724b
Revises: 4f831c1db811
Create Date: 2025-02-19 01:21:53.441746

"""
from typing import Sequence, Union

import sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32d98e7c724b'
down_revision: Union[str, None] = '4f831c1db811'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_NOTIFICATION', sa.Column('receive_date', sa.DateTime(), nullable=False, server_default=sqlalchemy.func.now()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('TBL_NOTIFICATION', 'receive_date')
    # ### end Alembic commands ###

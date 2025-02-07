"""empty message

Revision ID: 72d96bef66e1
Revises: 5f8f448de760
Create Date: 2025-02-07 15:01:43.595816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72d96bef66e1'
down_revision: Union[str, None] = '5f8f448de760'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_CART_PRODUCT', sa.Column('removed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('TBL_CART_PRODUCT', 'removed')
    # ### end Alembic commands ###

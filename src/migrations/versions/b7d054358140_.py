"""empty message

Revision ID: b7d054358140
Revises: c729ee39c732
Create Date: 2024-11-20 06:24:37.846739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b7d054358140'
down_revision: Union[str, None] = 'c729ee39c732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_PRODUCT', sa.Column('product_description', sa.String(length=255), nullable=False))
    op.add_column('TBL_PRODUCT', sa.Column('listing_date', sa.DateTime(), nullable=True))
    op.drop_column('TBL_PRODUCT', 'product_text')
    op.drop_column('TBL_PRODUCT', 'product_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_PRODUCT', sa.Column('product_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('TBL_PRODUCT', sa.Column('product_text', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('TBL_PRODUCT', 'listing_date')
    op.drop_column('TBL_PRODUCT', 'product_description')
    # ### end Alembic commands ###

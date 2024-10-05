"""empty message

Revision ID: 0fa600394e9a
Revises: 806d4e02b9c4
Create Date: 2024-09-12 00:43:18.706454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fa600394e9a'
down_revision: Union[str, None] = '806d4e02b9c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_CREATOR', sa.Column('product_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'TBL_CREATOR', 'TBL_PRODUCT', ['product_id'], ['product_id'])
    op.drop_constraint('TBL_PRODUCT_tag_id_fkey', 'TBL_PRODUCT', type_='foreignkey')
    op.drop_column('TBL_PRODUCT', 'tag_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_PRODUCT', sa.Column('tag_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('TBL_PRODUCT_tag_id_fkey', 'TBL_PRODUCT', 'TBL_TAG', ['tag_id'], ['tag_id'])
    op.drop_constraint(None, 'TBL_CREATOR', type_='foreignkey')
    op.drop_column('TBL_CREATOR', 'product_id')
    # ### end Alembic commands ###

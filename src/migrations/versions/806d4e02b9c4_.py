"""empty message

Revision ID: 806d4e02b9c4
Revises: bb524ab75a3d
Create Date: 2024-09-12 00:31:42.671219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '806d4e02b9c4'
down_revision: Union[str, None] = 'bb524ab75a3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_PRODUCT', sa.Column('tag_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'TBL_PRODUCT', 'TBL_TAG', ['tag_id'], ['tag_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'TBL_PRODUCT', type_='foreignkey')
    op.drop_column('TBL_PRODUCT', 'tag_id')
    # ### end Alembic commands ###

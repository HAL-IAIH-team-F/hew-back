"""empty message

Revision ID: 2519a0e70d14
Revises: 5db3890c939b
Create Date: 2024-12-07 22:39:05.978121

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2519a0e70d14'
down_revision: Union[str, None] = '5db3890c939b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TBL_NOTIFICATION', sa.Column('receive_user', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'TBL_NOTIFICATION', 'TBL_USER', ['receive_user'], ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'TBL_NOTIFICATION', type_='foreignkey')
    op.drop_column('TBL_NOTIFICATION', 'receive_user')
    # ### end Alembic commands ###

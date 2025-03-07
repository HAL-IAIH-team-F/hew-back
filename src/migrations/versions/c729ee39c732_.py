"""empty message

Revision ID: c729ee39c732
Revises: 7402e6c7d71e
Create Date: 2024-11-09 11:14:54.051001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c729ee39c732'
down_revision: Union[str, None] = '7402e6c7d71e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'TBL_CHAT_MESSAGE', ['chat_id', 'index'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'TBL_CHAT_MESSAGE', type_='unique')
    # ### end Alembic commands ###

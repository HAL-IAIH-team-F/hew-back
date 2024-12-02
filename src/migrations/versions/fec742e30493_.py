"""empty message

Revision ID: fec742e30493
Revises: b7d054358140
Create Date: 2024-11-28 23:42:58.673013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'fec742e30493'
down_revision: Union[str, None] = 'b7d054358140'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)

    # ### commands auto generated by Alembic - please adjust! ###
    if 'TBL_CHAT_MESSAGE' in inspector.get_table_names():
        op.add_column('TBL_CHAT_MESSAGE', sa.Column('post_user_id', sa.UUID(), nullable=False))
        op.alter_column('TBL_CHAT_MESSAGE', 'chat_id',
                   existing_type=sa.UUID(),
                   nullable=False)
        op.create_unique_constraint(None, 'TBL_CHAT_MESSAGE', ['index'])
        op.create_foreign_key(None, 'TBL_CHAT_MESSAGE', 'TBL_USER', ['post_user_id'], ['user_id'])

    if 'TBL_PRODUCT' in inspector.get_table_names():
        op.add_column('TBL_PRODUCT', sa.Column('purchase_date', sa.DateTime(), nullable=True))
        op.drop_column('TBL_PRODUCT', 'listing_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)
    # ### commands auto generated by Alembic - please adjust! ###
    if 'TBL_PRODUCT' in inspector.get_table_names():
        op.add_column('TBL_PRODUCT', sa.Column('listing_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        op.drop_column('TBL_PRODUCT', 'purchase_date')

    if 'TBL_CHAT_MESSAGE' in inspector.get_table_names():
        op.drop_constraint(None, 'TBL_CHAT_MESSAGE', type_='foreignkey')
        op.drop_constraint(None, 'TBL_CHAT_MESSAGE', type_='unique')
        op.alter_column('TBL_CHAT_MESSAGE', 'chat_id',
                   existing_type=sa.UUID(),
                   nullable=True)
        op.drop_column('TBL_CHAT_MESSAGE', 'post_user_id')
    # ### end Alembic commands ###

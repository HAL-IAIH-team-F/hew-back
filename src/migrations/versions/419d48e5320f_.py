"""empty message

Revision ID: 419d48e5320f
Revises: 476c6bdb459d
Create Date: 2024-11-10 20:10:50.904271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '419d48e5320f'
down_revision: Union[str, None] = '476c6bdb459d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TBL_NOTIFICATION',
    sa.Column('notification_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('TBL_PRODUCT',
    sa.Column('product_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('product_price', sa.Integer(), nullable=False),
    sa.Column('product_title', sa.String(length=64), nullable=False),
    sa.Column('product_text', sa.String(length=255), nullable=False),
    sa.Column('product_date', sa.DateTime(), nullable=True),
    sa.Column('product_thumbnail_uuid', sa.UUID(), nullable=False),
    sa.Column('product_contents_uuid', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('TBL_TAG',
    sa.Column('tag_id', sa.UUID(), nullable=False),
    sa.Column('tag_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('tag_id')
    )
    op.create_table('TBL_USER',
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_name', sa.String(length=64), nullable=False),
    sa.Column('user_screen_id', sa.String(length=64), nullable=False),
    sa.Column('user_icon_uuid', sa.UUID(), nullable=True),
    sa.Column('user_date', sa.DateTime(), nullable=True),
    sa.Column('user_mail', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('TBL_CART',
    sa.Column('cart_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('purchase_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['TBL_USER.user_id'], ),
    sa.PrimaryKeyConstraint('cart_id')
    )
    op.create_table('TBL_CREATOR',
    sa.Column('creator_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('contact_address', sa.String(length=64), nullable=False),
    sa.Column('transfer_target', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['TBL_USER.user_id'], ),
    sa.PrimaryKeyConstraint('creator_id')
    )
    op.create_table('TBL_LIKE',
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['TBL_PRODUCT.product_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['TBL_USER.user_id'], ),
    sa.PrimaryKeyConstraint('product_id', 'user_id')
    )
    op.create_table('TBL_PRODUCT_TAG',
    sa.Column('item_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['TBL_PRODUCT.product_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['TBL_TAG.tag_id'], ),
    sa.PrimaryKeyConstraint('item_id', 'tag_id')
    )
    op.create_table('TBL_PURCHASE',
    sa.Column('purchase_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('item_id', sa.UUID(), nullable=True),
    sa.Column('price', sa.String(length=64), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['TBL_PRODUCT.product_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['TBL_USER.user_id'], ),
    sa.PrimaryKeyConstraint('purchase_id')
    )
    op.create_table('TBL_CART_PRODUCT',
    sa.Column('cart_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['TBL_CART.cart_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['TBL_PRODUCT.product_id'], ),
    sa.PrimaryKeyConstraint('cart_id', 'product_id')
    )
    op.create_table('TBL_CREATOR_PRODUCT',
    sa.Column('creator_id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['TBL_CREATOR.creator_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['TBL_PRODUCT.product_id'], ),
    sa.PrimaryKeyConstraint('creator_id', 'product_id')
    )
    op.create_table('TBL_CREATOR_RECRUIT',
    sa.Column('creator_recruit_id', sa.UUID(), nullable=False),
    sa.Column('creator_id', sa.UUID(), nullable=False),
    sa.Column('contact_address', sa.String(length=64), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('context', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['TBL_CREATOR.creator_id'], ),
    sa.PrimaryKeyConstraint('creator_recruit_id')
    )
    op.create_table('TBL_NOTIFICATION_COLLABO',
    sa.Column('notification_id', sa.UUID(), nullable=False),
    sa.Column('sender_creator_id', sa.UUID(), nullable=False),
    sa.Column('sent_creator_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['notification_id'], ['TBL_NOTIFICATION.notification_id'], ),
    sa.ForeignKeyConstraint(['sender_creator_id'], ['TBL_CREATOR.creator_id'], ),
    sa.ForeignKeyConstraint(['sent_creator_id'], ['TBL_CREATOR.creator_id'], ),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('TBL_NOTIFICATION_PURCHASE',
    sa.Column('notification_id', sa.UUID(), nullable=False),
    sa.Column('purchase_user_id', sa.UUID(), nullable=False),
    sa.Column('sell_creator_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['notification_id'], ['TBL_NOTIFICATION.notification_id'], ),
    sa.ForeignKeyConstraint(['purchase_user_id'], ['TBL_USER.user_id'], ),
    sa.ForeignKeyConstraint(['sell_creator_id'], ['TBL_CREATOR.creator_id'], ),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('TBL_RANKING',
    sa.Column('creator_id', sa.UUID(), nullable=False),
    sa.Column('score', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['TBL_CREATOR.creator_id'], ),
    sa.PrimaryKeyConstraint('creator_id')
    )
    op.create_table('TBL_SERIALCODE',
    sa.Column('purchase_id', sa.UUID(), nullable=False),
    sa.Column('item_id', sa.UUID(), nullable=False),
    sa.Column('serial_code', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['TBL_PRODUCT.product_id'], ),
    sa.ForeignKeyConstraint(['purchase_id'], ['TBL_PURCHASE.purchase_id'], ),
    sa.PrimaryKeyConstraint('purchase_id', 'item_id')
    )
    op.create_table('TBL_USER_FOLLOW',
    sa.Column('follow_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('creator_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['TBL_CREATOR.creator_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['TBL_USER.user_id'], ),
    sa.PrimaryKeyConstraint('follow_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TBL_USER_FOLLOW')
    op.drop_table('TBL_SERIALCODE')
    op.drop_table('TBL_RANKING')
    op.drop_table('TBL_NOTIFICATION_PURCHASE')
    op.drop_table('TBL_NOTIFICATION_COLLABO')
    op.drop_table('TBL_CREATOR_RECRUIT')
    op.drop_table('TBL_CREATOR_PRODUCT')
    op.drop_table('TBL_CART_PRODUCT')
    op.drop_table('TBL_PURCHASE')
    op.drop_table('TBL_PRODUCT_TAG')
    op.drop_table('TBL_LIKE')
    op.drop_table('TBL_CREATOR')
    op.drop_table('TBL_CART')
    op.drop_table('TBL_USER')
    op.drop_table('TBL_TAG')
    op.drop_table('TBL_PRODUCT')
    op.drop_table('TBL_NOTIFICATION')
    # ### end Alembic commands ###

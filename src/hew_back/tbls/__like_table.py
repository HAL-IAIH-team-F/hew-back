import uuid

from sqlalchemy import Column, ForeignKey, UUID

from hew_back.db import BaseTable


# from asyncpg.pgproto.pgproto import UUID


class LikeTable(BaseTable):
    __tablename__ = 'TBL_LIKE'
    product_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), primary_key=True)

# # データベースエンジンの作成とテーブルの作成
# from sqlalchemy import create_engine
#
# engine = create_engine('sqlite:///likes.db')
# Base.metadata.create_all(engine)

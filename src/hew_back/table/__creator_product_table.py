import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base


from hew_back.db import BaseTable


class CreatorProductTable(BaseTable):
    __tablename__ = 'TBL_CREATOR_PRODUCT'
    creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True, default=uuid.uuid4)




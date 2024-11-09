import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from hew_back.db import BaseTable


class ProductTag(BaseTable):
    __tablename__ = 'TBL_PRODUCT_TAG'
    item_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True, default=uuid.uuid4)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('TBL_TAG.tag_id'), primary_key=True, default=uuid.uuid4)

from sqlalchemy import create_engine

# engine = create_engine('sqlite:///purchases.db')
# Base.metadata.create_all(engine)

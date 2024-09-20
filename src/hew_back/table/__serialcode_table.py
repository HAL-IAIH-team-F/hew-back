import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from hew_back.db import BaseTable


class SerialCodeTable(BaseTable):
    __tablename__ = 'TBL_SERIALCODE'
    purchase_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PURCHASE.purchase_id'), primary_key=True)
    # item_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True, default=uuid.uuid4)
    serial_code = Column(String(64), nullable=False, unique=False)




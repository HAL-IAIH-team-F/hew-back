import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base
import datetime

from hew_back.db import BaseTable


class PurchaseTable(BaseTable):
    __tablename__ = 'TBL_PURCHASE'

    purchase_id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=False, default=uuid.uuid4)
    price = Column(String(64), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False)



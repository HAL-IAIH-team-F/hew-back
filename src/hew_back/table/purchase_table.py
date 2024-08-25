from sqlalchemy import Column, Integer,uuid, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class PurchaseTable(Base):
    __tablename__ = 'TBL_PURCHASE'

    item_id = Column(Integer, ForeignKey('TBL_PRODUCT.product_id'), primary_key=False)
    purchase_id = Column(Integer, primary_key=False, default=False)
    price = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    user_id = Column(uuid.UUID, ForeignKey('TBL_USER.user_id'), nullable=False)



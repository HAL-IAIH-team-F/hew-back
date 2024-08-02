from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class PurchaseTable(Base):
    __tablename__ = 'TBL_PURCHASE'

    item_id = Column(String(64), ForeignKey('TBL_PRODUCT.product_id'), primary_key=False)
    purchase_id = Column(String(64), primary_key=False, autoincrement=False)
    price = Column(String(64), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = Column(String(64), ForeignKey('TBL_USER.user_id'), nullable=False)



from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SerialCodeTable(Base):
    __tablename__ = 'TBL_SERIALCODE'

    purchase_id = Column(String(64), ForeignKey('TBL_PURCHASE.purchase_id'), primary_key=True)
    serial_code = Column(String(64), nullable=False, unique=False)




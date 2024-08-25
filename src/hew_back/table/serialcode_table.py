from sqlalchemy import Column, uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SerialCodeTable(Base):
    __tablename__ = 'TBL_SERIALCODE'

    purchase_id = Column(uuid.UUID, ForeignKey('TBL_PURCHASE.purchase_id'), primary_key=True)
    serial_code = Column(uuid.UUID, nullable=False, unique=False)




from sqlalchemy import Column, uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProductTag(Base):
    __tablename__ = 'TBL_PRODUCT_TAG'
    item_id = Column(uuid.UUID, ForeignKey('TBL_PRODUCT.id'), primary_key=False)
    tag_id = Column(uuid.UUID, ForeignKey('TBL_TAG.tag_id'), primary_key=False)



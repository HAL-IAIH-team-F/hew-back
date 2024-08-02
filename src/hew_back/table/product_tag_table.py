from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProductTag(Base):
    __tablename__ = 'TBL_PRODUCT_TAG'
    item_id = Column(String(64), ForeignKey('product.id'), primary_key=False)
    tag_id = Column(String(64), ForeignKey('TBL_TAG.tag_id'), primary_key=False)

from sqlalchemy import create_engine

engine = create_engine('sqlite:///purchases.db')
Base.metadata.create_all(engine)

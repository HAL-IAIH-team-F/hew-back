from sqlalchemy import Column, uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductUserTable(Base):
    __tablename__ = 'TBL_USER_PRODUCT'

    user_id = Column(uuid.UUID, ForeignKey('TBL_USER.user_id'), primary_key=True,default=False)
    product_id = Column(uuid.UUID, ForeignKey('TBL_PRODUCT.product_id'), primary_key=True)




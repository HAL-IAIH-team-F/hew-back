from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'TBL_USER_PRODUCT'

    user_id = Column(String(64), ForeignKey('TBL_USER.user_id'), primary_key=True)
    product_id = Column(String(64), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True)




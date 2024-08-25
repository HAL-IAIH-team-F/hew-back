from sqlalchemy import Column, uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LikeTable(Base):
    __tablename__ = 'TBL_LIKE'

    product_id = Column(uuid.UUID, ForeignKey('TBL_PRODUCT.product_id'), primary_key=False)
    user_id = Column(uuid.UUID, ForeignKey('TBL_USER.user_id'), primary_key=False)



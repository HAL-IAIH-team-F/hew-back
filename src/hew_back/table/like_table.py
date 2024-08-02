from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LikeTable(Base):
    __tablename__ = 'TBL_LIKE'

    product_id = Column(Integer, ForeignKey('TBL_PRODUCT.product_id'), primary_key=False)
    user_id = Column(Integer, ForeignKey('TBL_USER.user_id'), primary_key=False)


# データベースエンジンの作成とテーブルの作成
from sqlalchemy import create_engine

engine = create_engine('sqlite:///likes.db')
Base.metadata.create_all(engine)

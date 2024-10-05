from sqlalchemy import Column,  String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class ProductTable(Base):
    __tablename__ = 'TBL_PRODUCT'

    product_id = Column(String(64), primary_key=False, autoincrement=False)
    product_price = Column(String(64), nullable=False)
    product_title = Column(String(64), nullable=False)
    product_text = Column(String(255), nullable=False)
    product_date = Column(DateTime, default=datetime.datetime.now)
    product_thumbnail_uuid = Column(String(36), nullable=False)
    product_contents_uuid = Column(String(36), nullable=False)


# データベースエンジンの作成とテーブルの作成
from sqlalchemy import create_engine

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)

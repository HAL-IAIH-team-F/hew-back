from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'TBL_USER'

    user_id = Column(String(64), primary_key=False, autoincrement=False)
    user_name = Column(String(64), nullable=False)
    user_screen_id = Column(String(64), nullable=False, unique=False)
    user_icon_uuid = Column(String(36), nullable=True)
    user_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_mail = Column(String(64), nullable=False, unique=False)


# データベースエンジンの作成とテーブルの作成
from sqlalchemy import create_engine

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)

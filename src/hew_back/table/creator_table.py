
from sqlalchemy import Column,  String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CreatorTable(Base):
    __tablename__ = 'TBL_CREATOR'  # テーブル名の修正
    user_id = Column(String(64), ForeignKey('TBL_USER.user_id'), primary_key=True)
    contact_address = Column(String(64), nullable=False)
    transfer_target = Column(String(64), nullable=False)

# データベースエンジンの作成とテーブルの作成
from sqlalchemy import create_engine

engine = create_engine('sqlite:///creators.db')
Base.metadata.create_all(engine)

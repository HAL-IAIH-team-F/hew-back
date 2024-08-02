from sqlalchemy import Column,  String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CreatorRecruitTable(Base):
    __tablename__ = 'TBL_CREATOR_RECRUIT'  # テーブル名を修正

    user_id = Column(String(64),primary_key=False, nullable=False)
    contact_address = Column(String(64), nullable=False)
    title = Column(String(64), nullable=False)
    context = Column(String(255), nullable=False)



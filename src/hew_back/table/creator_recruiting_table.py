from sqlalchemy import Column,  uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CreatorRecruitTable(Base):
    __tablename__ = 'TBL_CREATOR_RECRUIT'  # テーブル名を修正

    user_id = Column(uuid.UUID,primary_key=False, nullable=False)
    contact_address = Column(uuid.UUID, nullable=False)
    title = Column(uuid.UUID, nullable=False)
    context = Column(uuid.UUID, nullable=False)



from sqlalchemy import Column, uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ranking(Base):
    __tablename__ = 'TBL_RANKING'
    score = Column(uuid.UUID, nullable=False)
    user_id = Column(uuid.UUID, ForeignKey('TBL_USER.id'), primary_key=False)

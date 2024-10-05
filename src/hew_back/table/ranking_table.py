from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ranking(Base):
    __tablename__ = 'TBL_RANKING'
    score = Column(String(64), nullable=False)
    user_id = Column(String(64), ForeignKey('user.id'), primary_key=False)

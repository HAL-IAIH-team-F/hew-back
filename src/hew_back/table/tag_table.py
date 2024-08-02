from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'TBL_TAG'
    tag_id = Column(String(64), primary_key=True)
    tag_name = Column(String(64), nullable=False)

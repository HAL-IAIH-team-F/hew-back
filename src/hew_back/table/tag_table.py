from sqlalchemy import Column, uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'TBL_TAG'
    tag_id = Column(uuid.UUID, primary_key=True)
    tag_name = Column(uuid.UUID, nullable=False)

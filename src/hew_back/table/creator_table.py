
from sqlalchemy import Column,  uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CreatorTable(Base):
    __tablename__ = 'TBL_CREATOR'  # テーブル名の修正
    user_id = Column(uuid.UUID, ForeignKey('TBL_USER.user_id'), primary_key=True)
    contact_address = Column(uuid.UUID, ForeignKey('TBL_USER.user_id'),nullable=False)
    transfer_target = Column(uuid.UUID, ForeignKey('TBL_USER.user_id'), nullable=False)



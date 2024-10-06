import uuid

from sqlalchemy import Column,  String, ForeignKey, UUID, ForeignKey
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from hew_back.db import BaseTable

from sqlalchemy.orm import Mapped
class CreatorTable(BaseTable):
    __tablename__ = 'TBL_CREATOR'  # テーブル名の修正
    creator_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID]  = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False)
    contact_address = Column(String(64), nullable=False)
    transfer_target = Column(String(64), nullable=False) # 振込先




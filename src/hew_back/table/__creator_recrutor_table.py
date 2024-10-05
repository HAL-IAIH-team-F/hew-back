import uuid

# # from asyncpg.pgproto.pgproto import UUID
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base


from hew_back.db import BaseTable


class CreatorRecruitTable(BaseTable):
    __tablename__ = 'TBL_CREATOR_RECRUIT'  # テーブル名を修正
    creator_recruit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4)
    contact_address = Column(String(64), nullable=False)
    title = Column(String(64), nullable=False)
    context = Column(String(255), nullable=False)

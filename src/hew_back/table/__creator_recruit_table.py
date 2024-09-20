import uuid

# # from asyncpg.pgproto.pgproto import UUID
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base


from hew_back.db import BaseTable


class CreatorRecruitTable(BaseTable):
    __tablename__ = 'TBL_CREATOR_RECRUIT'
    recruiting_id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4)  # 募集そのもののID
    recruiting_creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False,
                               default=uuid.uuid4)  # コラボを募集するクリエイター
    title = Column(String(64), nullable=False)
    context = Column(String(255), nullable=False)

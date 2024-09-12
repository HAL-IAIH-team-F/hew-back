import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from hew_back.db import BaseTable


class Ranking(BaseTable):
    __tablename__ = 'TBL_RANKING'
    creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), primary_key=True, default=uuid.uuid4)
    score = Column(String(64), nullable=False)

import uuid

from sqlalchemy import Column, String, ForeignKey, UUID

from hew_back.db import BaseTable


# from asyncpg.pgproto.pgproto import UUID


class Ranking(BaseTable):
    __tablename__ = 'TBL_RANKING'
    creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), primary_key=True, default=uuid.uuid4)
    score = Column(String(64), nullable=False)

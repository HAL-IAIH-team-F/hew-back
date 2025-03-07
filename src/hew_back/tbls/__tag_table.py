import uuid

from sqlalchemy import Column, String, UUID

from hew_back.db import BaseTable


# from asyncpg.pgproto.pgproto import UUID


class Tag(BaseTable):
    __tablename__ = 'TBL_TAG'
    tag_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag_name = Column(String(64), nullable=False)

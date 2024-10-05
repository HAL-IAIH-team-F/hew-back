import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from hew_back.db import BaseTable


class NotificationTable(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION'

    notification_id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4)




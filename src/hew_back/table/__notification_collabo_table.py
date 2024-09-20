import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from hew_back.db import BaseTable


class NotificationCollaboTable(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION_COLLABO'

    notification_id = Column(UUID(as_uuid=True), ForeignKey('TBL_NOTIFICATION.notification_id'),
                             nullable=False, default=uuid.uuid4)
    # 送り元クリエイターID
    sender_creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4)
    # 送り先クリエイターID
    sent_creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4)


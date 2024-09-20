import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from hew_back.db import BaseTable


class NotificationPurchase(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION_PURCHASE'

    notification_id = Column(UUID(as_uuid=True), ForeignKey('TBL_NOTIFICATION.notification_id'),
                             nullable=False, default=uuid.uuid4)
    # 購入者
    purchase_user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False, default=uuid.uuid4)
    # 出品者
    sell_creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4)

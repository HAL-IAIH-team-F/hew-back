import dataclasses
import uuid

import sqlalchemy
from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class NotificationTable(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION'

    notification_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    receive_user: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), sqlalchemy.ForeignKey('TBL_USER.user_id'), nullable=False, default=uuid.uuid4
    )
    read: Mapped[bool] = Column(sqlalchemy.Boolean, nullable=False, default=False)

@dataclasses.dataclass
class CollaboNotificationTable(BaseTable):
    __tablename__ = 'TBL_COLLABO_NOTIFICATION'

    notification_collabo_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    notification_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_NOTIFICATION.notification_id'), primary_key=True, nullable=False,
        default=uuid.uuid4
    )
    sender_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4
    )
    receive_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4
    )

@dataclasses.dataclass
class ApproveNotificationTable(BaseTable):
    __tablename__ = 'TBL_APPROVE_NOTIFICATION'

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    notification_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_NOTIFICATION.notification_id'), primary_key=True, nullable=False,
        default=uuid.uuid4
    )
    collabo_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_COLLABO_NOTIFICATION.notification_collabo_id'), nullable=False
    )

class NotificationPurchase(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION_PURCHASE'

    notification_id = Column(UUID(as_uuid=True), ForeignKey('TBL_NOTIFICATION.notification_id'), primary_key=True,
                             nullable=False, default=uuid.uuid4)
    # 購入者
    purchase_user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False, default=uuid.uuid4)
    # 出品者
    sell_creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4)

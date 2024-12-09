import dataclasses
import uuid

import sqlalchemy
from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class NotificationTable(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION'
    __table_args__ = (
        sqlalchemy.CheckConstraint("""
        CASE collabo_id WHEN NULL THEN 0 ELSE 1 END 
        + CASE collabo_approve_id WHEN NULL THEN 0 ELSE 1 END 
        = 1
        ""","check_notification_children"),
    )
    notification_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    receive_user: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), sqlalchemy.ForeignKey('TBL_USER.user_id'), nullable=False
    )
    read: Mapped[bool] = Column(sqlalchemy.Boolean, nullable=False, default=False)

    collabo_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), sqlalchemy.ForeignKey('TBL_COLLABO.collabo_id'), nullable=True
    )
    collabo_approve_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), sqlalchemy.ForeignKey('TBL_COLLABO_APPROVE.approve_id'), nullable=True
    )



class NotificationPurchase(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION_PURCHASE'

    notification_id = Column(UUID(as_uuid=True), ForeignKey('TBL_NOTIFICATION.notification_id'), primary_key=True,
                             nullable=False, default=uuid.uuid4)
    # 購入者
    purchase_user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False, default=uuid.uuid4)
    # 出品者
    sell_creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False,
                             default=uuid.uuid4)

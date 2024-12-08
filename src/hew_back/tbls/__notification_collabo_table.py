import dataclasses
import uuid

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class NotificationCollaboTable(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION_COLLABO'

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

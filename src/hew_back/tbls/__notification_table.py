import dataclasses
import uuid

from sqlalchemy import Column, UUID
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class NotificationTable(BaseTable):
    __tablename__ = 'TBL_NOTIFICATION'

    notification_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )

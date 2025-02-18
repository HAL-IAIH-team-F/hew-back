import dataclasses
import datetime
import uuid

from sqlalchemy import Column, UUID, ForeignKey, DateTime
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class CartTable(BaseTable):
    __tablename__ = 'TBL_CART'
    cart_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'))
    purchase_date: Mapped[datetime.datetime | None] = Column(DateTime, nullable=True)

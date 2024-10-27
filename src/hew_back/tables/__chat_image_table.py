import uuid

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


class ChatImageTable(BaseTable):
    __tablename__ = 'TBL_CHAT_IMAGE'
    chat_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CHAT.chat_id'), primary_key=True)
    image_uuid: Mapped[uuid.UUID | None] = Column(UUID(as_uuid=True), nullable=True)

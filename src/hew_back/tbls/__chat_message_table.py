import uuid

import sqlalchemy
from sqlalchemy import Column, ForeignKey, UUID

from hew_back.db import BaseTable


class ChatMessageTable(BaseTable):
    __tablename__ = 'TBL_CHAT_MESSAGE'
    chat_message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CHAT.chat_id'))
    index = Column(sqlalchemy.Integer, nullable=False)
    message = Column(sqlalchemy.Text, nullable=False)

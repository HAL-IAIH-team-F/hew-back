import uuid

import sqlalchemy
from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.db import BaseTable


class ChatTable(BaseTable):
    __tablename__ = 'TBL_CHAT'
    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    to_user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'))
    message = Column(sqlalchemy.Text, nullable=False)

    def save_new(self, session: AsyncSession):
        session.add(self)

    @staticmethod
    def create(
            to_user: tbls.UserTable,
            message: str,
    ) -> 'ChatTable':
        return ChatTable(
            to_user_id=to_user.user_id,
            message=message,
        )

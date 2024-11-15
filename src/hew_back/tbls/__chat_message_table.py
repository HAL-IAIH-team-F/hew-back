import uuid

import sqlalchemy
from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.db import BaseTable


class ChatMessageTable(BaseTable):
    __tablename__ = 'TBL_CHAT_MESSAGE'
    __table_args__ = (
        sqlalchemy.UniqueConstraint("chat_id", "index"),
    )
    chat_message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CHAT.chat_id'))
    index = Column(sqlalchemy.Integer, nullable=False)
    message = Column(sqlalchemy.Text, nullable=False)

    @staticmethod
    async def find_messages(session: AsyncSession, chat: tbls.ChatTable, user: tbls.UserTable):
        res = await session.execute(
            sqlalchemy.select(ChatMessageTable)
            .distinct()
            .join(tbls.ChatUserTable, ChatMessageTable.chat_id == tbls.ChatUserTable.chat_id)
            .where(sqlalchemy.and_(
                ChatMessageTable.chat_id == chat.chat_id,
                tbls.ChatUserTable.user_id == user.user_id,
            ))
            .order_by(ChatMessageTable.index)
        )
        records = res.scalars().all()
        return records

    @staticmethod
    async def last_index(session: AsyncSession, chat: tbls.ChatTable):
        res = await session.execute(
            sqlalchemy.select(sqlalchemy.func.max(ChatMessageTable.index))
            .where(ChatMessageTable.chat_id == chat.chat_id)
        )
        num = res.scalar_one_or_none()
        if num is None:
            return 0
        return num

    @staticmethod
    def create(
            session: AsyncSession,
            chat: tbls.ChatTable,
            index: int,
            message: str,
    ) -> 'ChatMessageTable':
        table = ChatMessageTable(
            chat_id=chat.chat_id,
            message=message,
            index=index,
        )
        session.add(table)
        return table

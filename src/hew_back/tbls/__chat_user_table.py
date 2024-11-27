import uuid

import sqlalchemy
from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from hew_back import tbls
from hew_back.db import BaseTable


class ChatUserTable(BaseTable):
    __tablename__ = 'TBL_CHAT_USER'
    chat_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey('TBL_CHAT.chat_id'), primary_key=True)
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), primary_key=True)

    @staticmethod
    def create(
            chat: tbls.ChatTable,
            user: tbls.UserTable,
            session: AsyncSession
    ) -> 'ChatUserTable':
        table = ChatUserTable(
            chat_id=chat.chat_id,
            user_id=user.user_id,
        )
        session.add(table)
        return table

    @staticmethod
    def create_all(
            chat: tbls.ChatTable,
            users: list[tbls.UserTable],
            session: AsyncSession
    ) -> list['ChatUserTable']:
        tables: list[ChatUserTable] = []
        for user in users:
            table = ChatUserTable.create(chat, user, session)
            tables.append(table)
        return tables

    @staticmethod
    async def find_all_by_chat(session: AsyncSession, user: tbls.ChatTable) -> list['ChatUserTable']:
        res = await session.execute(
            sqlalchemy.select(ChatUserTable)
            .where(tbls.ChatUserTable.chat_id == user.chat_id)
        )
        tables: list[ChatUserTable] = []
        for tbl in res.scalars().all():
            tables.append(tbl)
        return tables

import uuid

import sqlalchemy
from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.db import BaseTable


class ChatUserTable(BaseTable):
    __tablename__ = 'TBL_CHAT_USER'
    chat_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CHAT.chat_id'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), primary_key=True)

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

import uuid

import sqlalchemy
from sqlalchemy import Column, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.db import BaseTable


class ChatTable(BaseTable):
    __tablename__ = 'TBL_CHAT'
    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @staticmethod
    async def find_all(session: AsyncSession, user: tbls.UserTable) -> list['ChatTable']:
        res = await session.execute(
            sqlalchemy.select(ChatTable)
            .distinct()
            .join(tbls.ChatUserTable)
            .where(tbls.ChatUserTable.user_id == user.user_id)
        )
        tables: list[ChatTable] = []
        for tbl in res.scalars().all():
            tables.append(tbl)
        return tables

    @staticmethod
    def create(
            session: AsyncSession
    ) -> 'ChatTable':
        table = ChatTable()
        session.add(table)
        return table

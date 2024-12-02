import uuid

import sqlalchemy
from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from hew_back import tbls
from hew_back.db import BaseTable


class ChatImageTable(BaseTable):
    __tablename__ = 'TBL_CHAT_IMAGE'
    chat_message_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CHAT_MESSAGE.chat_message_id'), primary_key=True)
    image_uuid: Mapped[uuid.UUID | None] = Column(UUID(as_uuid=True), nullable=True)

    @staticmethod
    async def find_messages(session: AsyncSession, message: tbls.ChatMessageTable):
        res = await session.execute(
            sqlalchemy.select(ChatImageTable)
            .where(ChatImageTable.chat_message_id == message.chat_message_id)
        )
        records = res.scalars().all()
        return records

    @staticmethod
    def create(
            message: tbls.ChatMessageTable,
            image_uuid: uuid.UUID,
            session: AsyncSession
    ) -> 'ChatImageTable':
        table = ChatImageTable(
            chat_message_id=message.chat_message_id,
            image_uuid=image_uuid,
        )
        session.add(table)
        return table

    @staticmethod
    def create_all(
            chat: tbls.ChatTable,
            image_uuids: list[uuid.UUID],
            session: AsyncSession
    ) -> list['ChatImageTable']:
        tbls: list[ChatImageTable] = []
        for image_uuid in image_uuids:
            table = ChatImageTable.create(chat, image_uuid, session)
            tbls.append(table)
        return tbls

import uuid

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from hew_back import tbls
from hew_back.db import BaseTable


class ChatImageTable(BaseTable):
    __tablename__ = 'TBL_CHAT_IMAGE'
    chat_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CHAT.chat_id'), primary_key=True)
    image_uuid: Mapped[uuid.UUID | None] = Column(UUID(as_uuid=True), nullable=True)

    @staticmethod
    def create(
            chat: tbls.ChatTable,
            image_uuid: uuid.UUID,
            session: AsyncSession
    ) -> 'ChatImageTable':
        table = ChatImageTable(
            chat_id=chat.chat_id,
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
        tables: list[ChatImageTable] = []
        for image_uuid in image_uuids:
            table = ChatImageTable.create(chat, image_uuid, session)
            tables.append(table)
        return tables

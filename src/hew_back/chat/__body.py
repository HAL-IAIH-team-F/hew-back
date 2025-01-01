import uuid

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls
from hew_back.chat.__result import ChatMessageResult


class PostChatMessageBody(BaseModel):
    message: str
    images: list[uuid.UUID]

    async def save_new(self, session: AsyncSession, chat_id: uuid.UUID, user: deps.UserDeps) -> ChatMessageResult:
        chat = await tbls.ChatTable.find(session, chat_id, user.user_table)

        last_index = await tbls.ChatMessageTable.last_index(session, chat)
        chat_message = tbls.ChatMessageTable.create(session, chat, last_index + 1, self.message, user.user_table)
        await session.flush()
        await session.refresh(chat_message)
        images = tbls.ChatImageTable.create_all(chat, self.images, session)
        await session.flush()
        for image in images:
            await session.refresh(image)

        return ChatMessageResult(
            chat, chat_message, images
        )

import uuid

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls
from hew_back.chat.__result import ChatUsersResult, ChatMessageResult


class PostChatBody(BaseModel):
    users: list[uuid.UUID]

    async def save_new(self, user: deps.UserDeps, session: AsyncSession) -> ChatUsersResult:
        users = tbls.UserTable.find_all(session, self.users)

        chat = tbls.ChatTable.create(session)
        await session.commit()
        await session.refresh(chat)
        users = await  users
        users.append(user.user_table)
        for user in users:
            await session.refresh(user)

        users = tbls.ChatUserTable.create_all(chat, users, session)
        await session.commit()
        for user in users:
            await session.refresh(user)
        await session.refresh(chat)

        return ChatUsersResult(
            chat, users
        )


class PostChatMessageBody(BaseModel):
    message: str
    images: list[uuid.UUID]

    async def save_new(self, session: AsyncSession, chat_id: uuid.UUID) -> ChatMessageResult:
        chat = await tbls.ChatTable.find(session, chat_id)

        last_index = await tbls.ChatMessageTable.last_index(session, chat)
        chat_message = tbls.ChatMessageTable.create(session, chat, last_index + 1, self.message)
        await session.flush()
        await session.refresh(chat_message)
        images = tbls.ChatImageTable.create_all(chat, self.images, session)
        await session.flush()
        for image in images:
            await session.refresh(image)

        return ChatMessageResult(
            chat, chat_message, images
        )

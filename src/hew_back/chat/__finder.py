import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, deps
from hew_back.chat.__result import MessageResult, ChatMessagesResult


class ChatFinder:
    @staticmethod
    async def find_chat_messages(
            session: AsyncSession,
            chat_id: uuid.UUID,
            user: deps.UserDeps
    ) -> ChatMessagesResult:
        chat = await tbls.ChatTable.find(session, chat_id, user.user_table)
        messages = await tbls.ChatMessageTable.find_messages(session, chat, user.user_table)
        result: list[MessageResult] = []
        for message in messages:
            result.append(await ChatFinder.find_images(session, message))
        return ChatMessagesResult(
            chat, result
        )

    @staticmethod
    async def find_images(session: AsyncSession, message: tbls.ChatMessageTable) -> MessageResult:
        images = await tbls.ChatImageTable.find_messages(session, message)
        return MessageResult(
            message, images
        )

import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.chat.__res import ChatRes


@dataclass
class ChatUsersResult:
    chat: tbls.ChatTable
    users: list[tbls.ChatUserTable]

    def to_chat_res(self) -> ChatRes:
        user_ids: list[uuid.UUID] = []
        for chat_user in self.users:
            user_ids.append(chat_user.user_id)
        return ChatRes.create(self.chat.chat_id, user_ids)


@dataclass
class ChatsResult:
    chats: list[ChatUsersResult]

    def to_chat_reses(self) -> list[ChatRes]:
        result: list[ChatRes] = []
        for chat in self.chats:
            result.append(chat.to_chat_res())
        return result


@dataclass
class MessageResult:
    message: tbls.ChatMessageTable
    images: list[tbls.ChatImageTable]


@dataclass
class ChatMessagesResult:
    chat: tbls.ChatTable
    messages: list[MessageResult]


@dataclass
class ChatMessageResult:
    chat: tbls.ChatTable
    message: tbls.ChatMessageTable
    images: list[tbls.ChatImageTable]

    async def refresh(self, session: AsyncSession):
        for wait in [
            session.refresh(self.chat),
            session.refresh(self.message),
            *map(lambda image: session.refresh(image), self.images),
        ]:
            await wait

import uuid
from dataclasses import dataclass

from hew_back import tbls
from hew_back.chat.__res import ChatRes, ChatMessageRes, MessageRes, ChatMessagesRes


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

    def to_message_res(self) -> MessageRes:
        images: list[uuid.UUID] = []
        for image in self.images:
            images.append(image.image_uuid)
        return MessageRes.create(
            self.message.chat_message_id,
            self.message.index,
            self.message.message,
            images
        )


@dataclass
class ChatMessagesResult:
    chat: tbls.ChatTable
    messages: list[MessageResult]

    def to_chat_messages_res(self) -> ChatMessagesRes:
        messages: list[MessageRes] = []
        for message in self.messages:
            messages.append(message.to_message_res())
        return ChatMessagesRes.create(
            self.chat.chat_id,
            messages
        )


@dataclass
class ChatMessageResult:
    chat: tbls.ChatTable
    message: tbls.ChatMessageTable
    images: list[tbls.ChatImageTable]

    def to_chat_message_res(self) -> ChatMessageRes:
        images: list[uuid.UUID] = []
        for image in self.images:
            images.append(image.image_uuid)
        return ChatMessageRes.create(
            self.chat.chat_id,
            self.message.chat_message_id,
            self.message.index,
            self.message.message,
            images
        )

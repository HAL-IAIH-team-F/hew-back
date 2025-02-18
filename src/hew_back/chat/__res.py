import uuid

import pydantic.dataclasses
from pydantic import BaseModel


class ChatRes(BaseModel):
    chat_id: uuid.UUID
    users: list[uuid.UUID]

    @staticmethod
    def create(
            chat_id: uuid.UUID,
            users: list[uuid.UUID],
    ):
        return ChatRes(
            chat_id=chat_id,
            users=users,
        )


@pydantic.dataclasses.dataclass
class MessageRes:
    chat_message_id: uuid.UUID
    index: int
    message: str
    images: list[uuid.UUID]
    post_user_id: uuid.UUID


class ChatMessagesRes(BaseModel):
    chat_id: uuid.UUID
    messages: list[MessageRes]

    @staticmethod
    def create(
            chat_id: uuid.UUID,
            messages: list[MessageRes]
    ):
        return ChatMessagesRes(
            chat_id=chat_id,
            messages=messages,
        )

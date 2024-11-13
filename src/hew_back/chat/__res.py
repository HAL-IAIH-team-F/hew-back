import uuid

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


class ChatMessageRes(BaseModel):
    chat_id: uuid.UUID
    chat_message_id: uuid.UUID
    index: int
    message: str
    images: list[uuid.UUID]

    @staticmethod
    def create(
            chat_id: uuid.UUID,
            chat_message_id: uuid.UUID,
            index: int,
            message: str,
            images: list[uuid.UUID],
    ):
        return ChatMessageRes(
            chat_id=chat_id,
            chat_message_id=chat_message_id,
            index=index,
            message=message,
            images=images,
        )

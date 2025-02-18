import uuid

import sqlalchemy
from fastapi import Depends

from hew_back import deps, tbls
from hew_back.chat.__res import MessageRes
from hew_back.chat.__result import ChatUsersResult


class ChatService:
    @staticmethod
    def create_message_res(
            message: tbls.ChatMessageTable,
            images: list[uuid.UUID],
    ):
        return MessageRes(
            chat_message_id=message.chat_message_id,
            index=message.index,
            message=message.message,
            images=images,
            post_user_id=message.post_user_id
        )

    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
    ):
        self.__session = session
        self.user = user

    async def create_chat(self, user_ids: list[uuid.UUID]):
        chat = tbls.ChatTable()
        self.__session.add(chat)
        await self.__session.flush()
        await self.__session.refresh(chat)

        chat = tbls.ChatTable.create(self.__session)
        await self.__session.flush()
        await self.__session.refresh(chat)

        chat_users: list[tbls.ChatUserTable] = []
        print(user_ids)
        for user_id in user_ids:
            table = tbls.ChatUserTable(
                chat_id=chat.chat_id,
                user_id=user_id,
            )
            self.__session.add(table)
            chat_users.append(table)

        await self.__session.flush()
        for chat_user in chat_users:
            await self.__session.refresh(chat_user)

        return ChatUsersResult(
            chat, chat_users
        )

import uuid

import pydantic
import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps, chat, tbls
from hew_back.chat.__res import ChatRes


@pydantic.dataclasses.dataclass
class PostChatBody:
    users: list[uuid.UUID]


class __Service:
    def __init__(
            self,
            body: PostChatBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            chat_service: chat.ChatService = Depends(),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
    ):
        self.__session = session
        self.__user = user
        self.__body = body
        self.__chat_service = chat_service

    async def process(self):
        users = tbls.UserTable.find_all(self.__session, self.__body.users)
        users = await  users
        users.append(self.__user.user_table)
        for user in users:
            await self.__session.refresh(user)
        res = await self.__chat_service.create_chat([u.user_id for u in users])
        return res.to_chat_res()


@app.post("/api/chat")
async def pc(
        service: __Service = Depends(),
) -> ChatRes:
    return await service.process()

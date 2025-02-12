import dataclasses
from typing import Union

import sqlalchemy

from hew_back import tbls
from .__token_deps import *
from .__db_deps import *
from .__file_token_deps import *
from .__img_deps import *
from ..chat.__result import ChatsResult, ChatUsersResult


@dataclasses.dataclass
class UserDeps:
    user_table: tbls.UserTable

    async def find_chats(self, session: AsyncSession) -> ChatsResult:
        chats = await tbls.ChatTable.find_all(session, self.user_table)
        items: list[ChatUsersResult] = []
        for chat in chats:
            users = await tbls.ChatUserTable.find_all_by_chat(session, chat)
            items.append(ChatUsersResult(chat, users))
        return ChatsResult(items)

    @staticmethod
    async def get_or_none(
            session: AsyncSession = Depends(DbDeps.session),
            token: JwtTokenDeps = Depends(JwtTokenDeps.get_access_token_or_none),
    ) -> Union['UserDeps', None]:
        if token is None:
            return None
        table = await tbls.UserTable.find_one_or_none(session, token.profile.sub)
        if table is None:
            return None
        table.user_mail = token.profile.email
        table.user_screen_id = token.profile.preferred_username
        await session.commit()
        await session.refresh(table)
        return UserDeps(table)

    @staticmethod
    async def get(
            session: AsyncSession = Depends(DbDeps.session),
            token: JwtTokenDeps = Depends(JwtTokenDeps.get_access_token),
    ) -> 'UserDeps':
        table = await tbls.UserTable.find_one(session, token.profile.sub)
        table.user_mail = token.profile.email
        table.user_screen_id = token.profile.preferred_username
        await session.commit()
        await session.refresh(table)
        return UserDeps(table)

    async def refresh(self, session: AsyncSession):
        for wait in [
            session.refresh(self.user_table),
        ]:
            await wait


async def _creator_table(
        session: AsyncSession = Depends(DbDeps.session),
        token: JwtTokenDeps = Depends(JwtTokenDeps.get_access_token),
) -> tbls.CreatorTable | None:
    res = await session.execute(
        sqlalchemy.select(tbls.CreatorTable)
        .where(tbls.CreatorTable.user_id == token.profile.sub)
    )
    return res.scalar_one_or_none()


class CreatorOrNoneDeps:
    creator_table: tbls.CreatorTable

    def __init__(
            self,
            creator: tbls.CreatorTable | None = Depends(_creator_table)
    ):
        self.creator_table = creator


class CreatorDeps:
    creator_table: tbls.CreatorTable

    def __init__(self, creator: tbls.CreatorTable):
        self.creator_table = creator

    @staticmethod
    async def get(
            session: AsyncSession = Depends(DbDeps.session),
            token: JwtTokenDeps = Depends(JwtTokenDeps.get_access_token),
    ) -> 'CreatorDeps':
        table = await tbls.CreatorTable.find_one(session, token.profile.sub)
        return CreatorDeps(table)

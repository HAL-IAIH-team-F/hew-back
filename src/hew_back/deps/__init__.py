from typing import Union

from hew_back import tbls, reses, results
from .__db_deps import *
from .__token_deps import *


@dataclass
class UserDeps:
    user_table: tbls.UserTable

    def to_self_user_res(self) -> reses.SelfUserRes:
        return reses.SelfUserRes.create_by_user_table(self.user_table)

    async def find_chats(self, session: AsyncSession) -> results.FindChatsResult:
        chats = await tbls.ChatTable.find_all(session, self.user_table)
        items: list[results.ChatUsersResult] = []
        for chat in chats:
            users = await tbls.ChatUserTable.find_all_by_chat(session, chat)
            items.append(results.ChatUsersResult(chat, users))
        return results.FindChatsResult(items)

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

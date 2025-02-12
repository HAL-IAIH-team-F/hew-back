from typing import Any, Coroutine

import sqlalchemy
from fastapi import Depends

from hew_back import deps, tbls, mdls
from hew_back.mdls import  CreatorData, UserData


class CreatorService:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
    ):
        self.session = session

    async def select_user(self, creator: tbls.CreatorTable) -> tbls.UserTable:
        row = await self.session.execute(
            sqlalchemy.select(tbls.UserTable)
            .where(tbls.UserTable.user_id == creator.user_id)
        )
        return row.scalar_one()

    @staticmethod
    def create_user_data(user: tbls.UserTable) -> UserData:
        return UserData(
            user_id=user.user_id,
            name=user.user_name,
            screen_id=user.user_screen_id,
            icon=mdls.File(
                image_uuid=user.user_icon_uuid,
                token=None,
            ),
        )
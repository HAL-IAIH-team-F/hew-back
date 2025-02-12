import uuid
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
        self.__session = session

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

    @staticmethod
    def create_creator_data(creator: tbls.CreatorTable | None) -> CreatorData | None:
        if creator is None:
            return None
        return CreatorData(
            creator_id=creator.creator_id,
            contact_address=creator.contact_address,
        )

    async def select_creator_or_none(self,user_id: uuid.UUID) -> tbls.CreatorTable:
        row = await self.__session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.user_id == user_id)
        )
        return row.scalar_one_or_none()

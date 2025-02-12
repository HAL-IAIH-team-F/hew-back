import uuid

import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls, mdls
from hew_back.creator.__creator_service import CreatorService
from hew_back.user.__res import SelfUserRes, UserRes
from hew_back.user.__user_service import UserService


class __Service:
    def __init__(
            self,
            user_id: uuid.UUID,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            user_service: UserService = Depends(),
            creator_service: CreatorService = Depends(),
    ):
        self.__session = session
        self.__user = user
        self.__user_service = user_service
        self.__user_id = user_id
        self.__creator_service = creator_service

    async def __select_user(self) -> tbls.UserTable:
        row = await self.__session.execute(
            sqlalchemy.select(tbls.UserTable)
            .where(tbls.UserTable.user_id == self.__user_id)
        )
        return row.scalar_one()

    async def process(self) -> SelfUserRes | UserRes:
        await self.__session.flush()
        creator = await self.__creator_service.select_creator_or_none(self.__user_id)
        if self.__user_id == self.__user.user_table.user_id:
            return UserService.create_user_res(
                self.__user.user_table,
                CreatorService.create_creator_data(creator),
            )
        else:
            user = await self.__select_user()
            return UserRes(
                user_id=user.user_id,
                name=user.user_name,
                screen_id=user.user_screen_id,
                icon=None if user.user_icon_uuid is None else mdls.File(
                    image_uuid=user.user_icon_uuid,
                    token=None,
                ),
                creator_data=CreatorService.create_creator_data(creator),
            )


@app.get("/api/user/{user_id}")
async def get_user___(
        service: __Service = Depends(),
) -> SelfUserRes | UserRes:
    return await service.process()

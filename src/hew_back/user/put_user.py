import fastapi
import sqlalchemy
from fastapi import Depends

from hew_back import app, deps, mdls
from hew_back.creator.__creator_service import CreatorService
from hew_back.user.__body import UserBody
from hew_back.user.__res import SelfUserRes
from hew_back.user.__user_service import UserService


class __Service:
    def __init__(
            self,
            body: UserBody,
            response: fastapi.Response,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            user_service: UserService = Depends(),
            creator_service: CreatorService = Depends(),
            img_deps: deps.ImageDeps = Depends(deps.ImageDeps.get),
    ):
        self.__session = session
        self.__user = user
        self.__response = response
        self.__user_service = user_service
        self.__body = body
        self.__creator_service = creator_service
        self.__img_deps = img_deps

    async def process(self) -> SelfUserRes:
        if self.__body.user_icon_uuid is not None:
            self.__img_deps.crete(mdls.State.public).post_preference(self.__body.user_icon_uuid)
        self.__user.user_table.user_icon_uuid = self.__body.user_icon_uuid
        self.__user.user_table.user_name = self.__body.user_name
        await self.__session.flush()
        creator = await self.__creator_service.select_creator_or_none(self.__user.user_table.user_id)
        return UserService.create_user_res(self.__user.user_table, CreatorService.create_creator_data(creator))


@app.put("/api/user")
async def put_user___(
        service: __Service = Depends(),
) -> SelfUserRes:
    return await service.process()

import fastapi
import sqlalchemy
from fastapi import Depends

from hew_back import app, deps, mdls
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
    ):
        self.__session = session
        self.__user = user
        self.__response = response
        self.__user_service = user_service
        self.__body = body

    async def process(self) -> SelfUserRes:
        self.__user.user_table.user_icon_uuid = self.__body.user_icon_uuid
        self.__user.user_table.user_name = self.__body.user_name
        if self.__body.user_icon_uuid is not None:
            await self.__user_service.post_images(self.__body.user_icon_uuid)
            user_icon = mdls.File(
                image_uuid=self.__user.user_table.user_icon_uuid,
                token=None,
            )
        else:
            user_icon = None
        await self.__session.flush()
        return SelfUserRes(
            user_id=self.__user.user_table.user_id,
            user_name=self.__user.user_table.user_name,
            user_screen_id=self.__user.user_table.user_screen_id,
            user_icon=user_icon,
            user_date=self.__user.user_table.user_date,
            user_mail=self.__user.user_table.user_mail,
        )


@app.put("/api/user")
async def put_user___(
        service: __Service = Depends(),
) -> SelfUserRes:
    return await service.process()

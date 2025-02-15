import sqlalchemy
from fastapi import Depends

from hew_back import mdls, deps, tbls
from hew_back.mdls import CreatorData
from hew_back.user.__res import SelfUserRes
from hew_back.util.pydanticutl import Uuid


class UserService:
    def __init__(
            self,
            img_deps: deps.ImageDeps = Depends(deps.ImageDeps.get),
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
    ):
        self.__session = session
        self.__img_deps = img_deps

    async def post_images(
            self,
            icon_uuid: Uuid,
    ):
        self.__img_deps.crete(mdls.State.public).post_preference(icon_uuid)

    async def select_user(self, creator: tbls.CreatorTable) -> tbls.UserTable:
        row = await self.__session.execute(
            sqlalchemy.select(tbls.UserTable)
            .where(tbls.UserTable.user_id == creator.user_id)
        )
        return row.scalar_one()

    @staticmethod
    def create_user_res(user: tbls.UserTable, creator_data: CreatorData) -> SelfUserRes:
        return SelfUserRes(
            user_id=user.user_id,
            name=user.user_name,
            screen_id=user.user_screen_id,
            icon=None if user.user_icon_uuid is None else mdls.File(
                image_uuid=user.user_icon_uuid,
                token=None,
            ),
            register_date=user.user_date,
            user_mail=user.user_mail,
            creator_data=creator_data,
        )

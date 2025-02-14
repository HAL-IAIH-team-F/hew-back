import uuid

import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls, mdls
from hew_back.creator.__res import CreatorResponse
from hew_back.mdls import UserData
from hew_back.user.__user_service import UserService


class __Service:
    def __init__(
            self,
            creator_id: uuid.UUID,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user_service: UserService = Depends(),
    ):
        self.session = session
        self.__creator_id = creator_id
        self.__user_service = user_service

    async def select_creator(self) -> tbls.CreatorTable:
        records = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id == self.__creator_id)
        )
        records = records.scalar_one()
        return records

    async def process(self) -> CreatorResponse:
        creator = await self.select_creator()
        user = await self.__user_service.select_user(creator)
        return CreatorResponse(
            creator_id=creator.creator_id,
            contact_address=creator.contact_address,
            user_data=UserData(
                user_id=user.user_id,
                name=user.user_name,
                screen_id=user.user_screen_id,
                icon=mdls.File(
                    image_uuid=user.user_icon_uuid,
                    token=None,
                ),
            )
        )


@app.get("/api/creator/{creator_id}")
async def getcre(
        service: __Service = Depends(),
) -> CreatorResponse:
    return await service.process()

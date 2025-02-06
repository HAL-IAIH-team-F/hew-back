import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.creator.__creator_service import CreatorService
from hew_back.creator.__res import CreatorResponse


class __Service:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            creator_service: CreatorService = Depends(),
    ):
        self.session = session
        self.__creator_service = creator_service

    async def select_creators(self) -> list[tbls.CreatorTable]:
        records = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
        )
        records = records.scalars().all()
        return [*records]

    async def process(self) -> list[CreatorResponse]:
        creators = await self.select_creators()
        return [CreatorResponse(
            creator_id=creator.creator_id,
            contact_address=creator.contact_address,
            user_data=self.__creator_service.create_user_data(await self.__creator_service.select_user(creator))
        ) for creator in creators]


@app.get("/api/creator")
async def gcs(
        service: __Service = Depends(),
) -> list[CreatorResponse]:
    return await service.process()

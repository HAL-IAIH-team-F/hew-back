import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.creator.__res import CreatorResponse
from test.conftest import session


class __Service:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
    ):
        self.session = session

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
            user_id=creator.user_id,
            contact_address=creator.contact_address,
            transfer_target=creator.transfer_target,
        ) for creator in creators]


@app.post("/api/creator")
async def pc(
        service: __Service = Depends(),
) -> list[CreatorResponse]:
    return await service.process()

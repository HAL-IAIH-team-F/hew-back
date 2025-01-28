import uuid

import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.creator.__res import CreatorResponse


class __Service:
    def __init__(
            self,
            creator_id: uuid.UUID,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
    ):
        self.session = session
        self.__creator_id = creator_id

    async def select_creators(self) -> tbls.CreatorTable:
        records = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id == self.__creator_id)
        )
        records = records.scalar_one()
        return records

    async def process(self) -> CreatorResponse:
        creator = await self.select_creators()
        return CreatorResponse(
            creator_id=creator.creator_id,
            user_id=creator.user_id,
            contact_address=creator.contact_address,
        )


@app.get("/api/creator/{creator_id}")
async def getcre(
        service: __Service = Depends(),
) -> CreatorResponse:
    return await service.process()

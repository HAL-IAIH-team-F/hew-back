import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls


@pydantic.dataclasses.dataclass
class PostColabApproveBody:
    colab_id: uuid.UUID


class Service:
    def __init__(
            self,
            body: PostColabApproveBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            sender: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
    ):
        self.session = session
        self.sender = sender
        self.body = body

    async def select_colab_creator(self) -> tbls.ColabCreatorTable:
        raw = await self.session.execute(
            sqlalchemy.select(tbls.ColabCreatorTable)
            .where(tbls.ColabCreatorTable.creator_id == self.sender.creator_table.creator_id)
            .where(tbls.ColabCreatorTable.collabo_id == self.body.colab_id)
        )
        return raw.scalar_one()

    async def insert_colab_approve(self) -> tbls.ColabApproveTable:
        colab_creator = await self.select_colab_creator()
        approve = tbls.ColabApproveTable(collabo_approve_id=colab_creator.collabo_creator_id)
        self.session.add(approve)
        await self.session.flush()
        await self.session.refresh(approve)
        return approve

    async def process(self):
        await self.insert_colab_approve()


@app.post("/api/colab/approve")
async def pca(
        service: Service = Depends(),
) -> None:
    return await service.process()

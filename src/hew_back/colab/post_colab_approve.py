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
        approve = tbls.ColabApproveTable(colab_creator_id=colab_creator.collabo_creator_id)
        self.session.add(approve)
        await self.session.flush()
        await self.session.refresh(approve)
        return approve

    async def select_owner(self) -> tbls.CreatorTable:
        raw = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .join(tbls.ColabTable, tbls.CreatorTable.creator_id == tbls.ColabTable.owner_creator_id)
            .where(tbls.ColabTable.collabo_id == self.body.colab_id)
        )
        return raw.scalar_one()

    async def insert_notification(self):
        approve = await self.insert_colab_approve()
        owner = await self.select_owner()
        notification = tbls.NotificationTable(
            receive_user=owner.user_id,
            collabo_approve_id=approve.collabo_approve_id,
        )
        self.session.add(notification)
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def process(self):
        await self.insert_notification()


@app.post("/api/colab/approve")
async def pca(
        service: Service = Depends(),
) -> None:
    return await service.process()

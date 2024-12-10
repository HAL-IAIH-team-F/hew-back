import dataclasses
import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.tbls import CollaboCreatorTable


@pydantic.dataclasses.dataclass
class PostCollaboBody:
    collabo_id: uuid.UUID
    approves: list[uuid.UUID]


@dataclasses.dataclass
class Record:
    request: tbls.ColabRequestTable
    approve: tbls.CollaboApproveTable


class __Service:
    def __init__(
            self,
            body: PostCollaboBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            sender: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
    ):
        self.session = session
        self.sender = sender
        self.body = body

    async def receiver(self, collabo: tbls.ColabRequestTable) -> tbls.CreatorTable:
        receiver_creator = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id == collabo.sender_creator_id)
        )
        return receiver_creator.scalar_one()

    async def select_approves_cloabs(self) -> list[Record]:
        st = await self.session.execute(
            sqlalchemy.select(tbls.CollaboApproveTable, tbls.ColabRequestTable)
            .select_from(tbls.CollaboApproveTable)
            .join(tbls.ColabRequestTable)
            .where(tbls.CollaboApproveTable.approve_id.in_(self.body.approves))
        )
        records = st.all()
        return [Record(
            record[0], record[1]
        ) for record in records]

    async def insert_colab(self) -> tbls.ColabTable:
        colab = tbls.ColabTable(
            owner_creator_id=self.sender.creator_table.creator_id,
        )
        self.session.add(colab)
        await self.session.flush()
        await self.session.refresh(colab)
        return colab

    async def insert_colab_creators(
            self,
    ) -> list[CollaboCreatorTable]:
        records = await self.select_approves_cloabs()
        colab = await self.insert_colab()
        colab_creators = list[tbls.CollaboCreatorTable]()
        for record in records:
            colab_creator = tbls.CollaboCreatorTable(
                creator_id=record.request.sender_creator_id,
                collabo_id=colab.collabo_id,
            )
            self.session.add(colab_creator)
            colab_creators.append(colab_creator)
        await self.session.flush()
        for colab_creator in colab_creators:
            await self.session.refresh(colab_creator)
        return colab_creators

    async def process(self):
        await self.insert_colab_creators()


@app.post("/api/colab")
async def pc(
        service: __Service = Depends(),
) -> None:
    return await service.process()

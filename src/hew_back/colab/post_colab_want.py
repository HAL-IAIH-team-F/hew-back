import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.creator.__creator_service import CreatorService


@pydantic.dataclasses.dataclass
class PostColabWantBody:
    target_creator_id: uuid.UUID


class Service:
    def __init__(
            self,
            body: PostColabWantBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            sender: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
            creator_service: CreatorService = Depends(),
    ):
        self.__session = session
        self.__sender = sender
        self.__body = body
        self.__creator_service = creator_service

    async def receiver(self, recruit: tbls.RecruitTable) -> tbls.CreatorTable:
        receiver_creator = await self.__session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id == recruit.creator_id)
        )
        return receiver_creator.scalar_one()

    async def insert_notification(
            self,
            target_creator: tbls.CreatorTable,
            colab_want: tbls.ColabWantTable,
    ) -> tbls.NotificationTable:
        notification = tbls.NotificationTable(
            receive_user=target_creator.user_id,
            collabo_want_id=colab_want.colab_want_id,
        )
        self.__session.add(notification)
        await self.__session.flush()
        await self.__session.refresh(notification)
        return notification

    async def insert_colab_want(
            self, target_creator: tbls.CreatorTable
    ) -> tbls.ColabWantTable:
        colab_want = tbls.ColabWantTable(
            sender_creator_id=self.__sender.creator_table.creator_id,
            receive_creator_id=target_creator.creator_id,
        )
        self.__session.add(colab_want)
        await self.__session.flush()
        await self.__session.refresh(colab_want)
        return colab_want

    async def process(self):
        target_creator = await self.__creator_service.select_creator(self.__body.target_creator_id)
        colab_want = await self.insert_colab_want(target_creator)
        await self.insert_notification(target_creator, colab_want)


@app.post("/api/colab/want")
async def post_colab_want__(
        service: Service = Depends(),
) -> None:
    return await service.process()

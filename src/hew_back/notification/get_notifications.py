import dataclasses
import uuid
from typing import List

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.notification.__reses import NotificationRes, NotificationType
from hew_back.util import err


@pydantic.dataclasses.dataclass
class PostColabRequestBody:
    recruit_id: uuid.UUID


@dataclasses.dataclass
class NotificationRecord:
    notification: tbls.NotificationTable
    collabo: tbls.NotificationCollaboTable | None


class Service:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
    ):
        self.session = session
        self.user = user

    async def select_notifications(self) -> list[NotificationRecord]:
        query = await self.session.execute(
            sqlalchemy.select(tbls.NotificationTable, tbls.NotificationCollaboTable)
            .where(tbls.NotificationTable.receive_user == self.user.user_table.user_id)
        )
        records = query.scalars().all()
        result = list[NotificationRecord]()
        for record in records:
            colab: tbls.NotificationCollaboTable | None = record
            if colab.sender_creator_id is None and colab.receive_creator_id is None:
                colab = None
            result.append(NotificationRecord(record, colab))

        return result

    async def notifications(self) -> list[NotificationRes]:
        notifications = await self.select_notifications()
        results = list[NotificationRes]()

        for notification in notifications:
            notification_type: NotificationType
            if notification.collabo is not None:
                notification_type = NotificationType.COLAB
            else:
                raise err.ErrorIds.NOTIFICATION_ERROR.to_exception("unknown notification type")
            results.append(NotificationRes(
                notification.notification.notification_id,
                notification_type

            ))
        return results


@app.post("/api/notification")
async def gns(
        service: Service = Depends(),
) -> list[NotificationRes]:
    return await service.notifications()

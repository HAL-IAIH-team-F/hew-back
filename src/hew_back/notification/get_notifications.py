import dataclasses
import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.notification.__reses import NotificationRes, NotificationType, ColabNotificationData
from hew_back.util import err


@pydantic.dataclasses.dataclass
class PostColabRequestBody:
    recruit_id: uuid.UUID


@dataclasses.dataclass
class NotificationRecord:
    notification: tbls.NotificationTable
    collabo: tbls.CollaboNotificationTable | None


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
            sqlalchemy.select(
                tbls.NotificationTable,
                tbls.CollaboNotificationTable,
            ).select_from(tbls.NotificationTable)
            .join(
                tbls.CollaboNotificationTable,
                tbls.CollaboNotificationTable.notification_id == tbls.NotificationTable.notification_id, isouter=True
            )
            .where(tbls.NotificationTable.receive_user == self.user.user_table.user_id)
        )
        records = query.all()
        result = list[NotificationRecord]()
        for record in records:
            colab: tbls.CollaboNotificationTable | None = record[1]
            result.append(NotificationRecord(record[0], colab))

        return result

    async def notifications(self) -> list[NotificationRes]:
        notifications = await self.select_notifications()
        results = list[NotificationRes]()

        for notification in notifications:
            notification_type: NotificationType
            data: ColabNotificationData
            if notification.collabo is not None:
                notification_type = NotificationType.COLAB
                data = ColabNotificationData(notification.collabo.sender_creator_id)
            else:
                raise err.ErrorIds.NOTIFICATION_ERROR.to_exception("unknown notification type")
            results.append(NotificationRes(
                notification.notification.notification_id,
                notification_type,
                data,
            ))
        return results


@app.get("/api/notification")
async def gns(
        service: Service = Depends(),
) -> list[NotificationRes]:
    return await service.notifications()

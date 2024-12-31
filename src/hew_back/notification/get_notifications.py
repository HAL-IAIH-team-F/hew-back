import dataclasses
import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.notification.__reses import NotificationRes, NotificationType, ColabRequestNotificationData, \
    ColabNotificationData
from hew_back.util import err


@pydantic.dataclasses.dataclass
class PostColabRequestBody:
    recruit_id: uuid.UUID


@dataclasses.dataclass
class NotificationRecord:
    notification: tbls.NotificationTable
    data: tbls.ColabRequestTable


class Service:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
    ):
        self.session = session
        self.user = user

    async def select_raw_notifications(self):
        query = await self.session.execute(
            sqlalchemy.select(
                tbls.NotificationTable,
                tbls.ColabRequestTable,
                tbls.ColabTable,
            ).select_from(tbls.NotificationTable)
            .join(
                tbls.ColabRequestTable,
                tbls.ColabRequestTable.collabo_request_id == tbls.NotificationTable.collabo_request_id, isouter=True
            )
            .join(
                tbls.ColabTable,
                tbls.ColabTable.collabo_id == tbls.NotificationTable.collabo_id, isouter=True
            )
            .where(tbls.NotificationTable.receive_user == self.user.user_table.user_id)
        )
        return query.all()

    async def select_notifications(self) -> list[NotificationRecord]:
        raw = await self.select_raw_notifications()
        result = list[NotificationRecord]()
        for record in raw:
            notification: tbls.NotificationTable = record[0]

            data: tbls.ColabRequestTable | None
            if notification.collabo_request_id is not None:
                data = record[1]
            elif notification.collabo_id is not None:
                data = record[2]
            else:
                raise err.ErrorIds.NOTIFICATION_ERROR.to_exception("unknown notification type 1")

            result.append(NotificationRecord(notification, data))

        return result

    async def select_colab_creators(self, colab: tbls.ColabTable) -> list[tbls.CollaboCreatorTable]:
        raw = await self.session.execute(
            sqlalchemy.select(tbls.CollaboCreatorTable)
            .where(tbls.CollaboCreatorTable.collabo_id == colab.collabo_id)
        )
        return [*raw.scalars().all()]

    async def notifications(self) -> list[NotificationRes]:
        notifications = await self.select_notifications()
        results = list[NotificationRes]()

        for notification in notifications:
            notification_type: NotificationType
            if isinstance(notification.data, tbls.ColabRequestTable):
                data = ColabRequestNotificationData(
                    notification_type=NotificationType.COLAB_REQUEST,
                    from_creator_id=notification.data.sender_creator_id,
                    colab_request_id=notification.data.collabo_request_id
                )
            elif isinstance(notification.data, tbls.ColabTable):
                creators = await self.select_colab_creators(notification.data)
                data = ColabNotificationData(
                    notification_type=NotificationType.COLAB,
                    collabo_id=notification.data.collabo_id,
                    owner_id=notification.data.owner_creator_id,
                    title=notification.data.title,
                    description=notification.data.description,
                    creator_ids=[c.creator_id for c in creators],
                )
            else:
                raise err.ErrorIds.NOTIFICATION_ERROR.to_exception("unknown notification type")
            results.append(NotificationRes(
                notification.notification.notification_id,
                data,
            ))
        return results


@app.get("/api/notification")
async def gns(
        service: Service = Depends(),
) -> list[NotificationRes]:
    return await service.notifications()

import dataclasses
import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.notification.__reses import NotificationRes, NotificationType, CollaboNotificationData, \
    CollaboApproveNotificationData
from hew_back.tbls import CollaboApproveTable
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

    async def select_notifications(self) -> list[NotificationRecord]:
        query = await self.session.execute(
            sqlalchemy.select(
                tbls.NotificationTable,
                tbls.ColabRequestTable,
                tbls.CollaboApproveTable,
            ).select_from(tbls.NotificationTable)
            .join(
                tbls.ColabRequestTable,
                tbls.ColabRequestTable.collabo_request_id == tbls.NotificationTable.collabo_request_id, isouter=True
            )
            .join(
                tbls.CollaboApproveTable,
                tbls.CollaboApproveTable.approve_id == tbls.NotificationTable.collabo_approve_id, isouter=True
            )
            .where(tbls.NotificationTable.receive_user == self.user.user_table.user_id)
        )
        records = query.all()
        result = list[NotificationRecord]()
        for record in records:
            notification: tbls.NotificationTable = record[0]

            data: tbls.ColabRequestTable | None
            if notification.collabo_request_id is not None:
                data = record[1]
            elif notification.collabo_approve_id is not None:
                data = record[2]
            else:
                raise err.ErrorIds.NOTIFICATION_ERROR.to_exception("unknown notification type 1")

            result.append(NotificationRecord(notification, data))

        return result

    async def notifications(self) -> list[NotificationRes]:
        notifications = await self.select_notifications()
        results = list[NotificationRes]()

        for notification in notifications:
            notification_type: NotificationType
            if isinstance(notification.data, tbls.ColabRequestTable):
                data = CollaboNotificationData(
                    notification_type=NotificationType.COLAB,
                    sender_creator_id=notification.data.sender_creator_id,
                    collabo_id=notification.data.collabo_request_id
                )
            elif isinstance(notification.data, tbls.CollaboApproveTable):
                data = CollaboApproveNotificationData(
                    notification_type=NotificationType.COLAB_APPROVE,
                    collabo_id=notification.data.collabo_id,
                    approve_id=notification.data.approve_id,
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

import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.notification.__notification_data_type import ColabNotificationDataType, ColabRequestNotificationDataType, \
    NotificationDataType, ColabApproveNotificationDataType
from hew_back.notification.__reses import NotificationRes, NotificationData
from hew_back.util import err


@pydantic.dataclasses.dataclass
class PostColabRequestBody:
    recruit_id: uuid.UUID


class Service:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            colab_notification: ColabNotificationDataType = Depends(),
            colab_request_notification: ColabRequestNotificationDataType = Depends(),
            colab_approve_notification: ColabApproveNotificationDataType = Depends(),
    ):
        self.session = session
        self.user = user
        self.notification_data_types: list[NotificationDataType] = [
            colab_notification, colab_request_notification, colab_approve_notification,
        ]

    async def select_raw_notifications(self):
        st = sqlalchemy.select(
            tbls.NotificationTable,
            *[t.table() for t in self.notification_data_types]
        ).select_from(tbls.NotificationTable)

        for data_type in self.notification_data_types:
            st = st.join(
                data_type.table(),
                data_type.join_condition(), isouter=True
            )

        query = await self.session.execute(
            st.where(tbls.NotificationTable.receive_user == self.user.user_table.user_id)
        )
        return query.all()

    async def notifications(self) -> list[NotificationRes]:
        raw = await self.select_raw_notifications()
        results = list[NotificationRes]()
        for record in raw:
            notification: tbls.NotificationTable = record[0]
            data: NotificationData | None = None
            for i in range(len(self.notification_data_types)):
                if self.notification_data_types[i].test_has_id(notification):
                    data = await self.notification_data_types[i].create_data(notification, record[i + 1])
                    break
            if data is None:
                raise err.ErrorIds.NOTIFICATION_ERROR.to_exception("unknown notification type 1")

            results.append(NotificationRes(
                notification.notification_id,
                data,
            ))

        return results


@app.get("/api/notification")
async def gns(
        service: Service = Depends(),
) -> list[NotificationRes]:
    return await service.notifications()

import abc

import sqlalchemy
from fastapi import Depends
from sqlalchemy import ColumnElement

from hew_back import tbls, deps
from hew_back.db import BaseTable
from hew_back.notification.__reses import NotificationData, ColabRequestNotificationData, NotificationType, \
    ColabNotificationData
from hew_back.tbls import ColabTable


class NotificationDataType[T: BaseTable](abc.ABC):
    @abc.abstractmethod
    def table(self) -> type[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def join_condition(self) -> ColumnElement[bool]:
        raise NotImplementedError

    @abc.abstractmethod
    def test_has_id(self, notification: tbls.NotificationTable) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_data(self, notification: tbls.NotificationTable, notification_data_table: T) -> NotificationData:
        raise NotImplementedError


class ColabNotificationDataType(NotificationDataType[tbls.ColabTable]):

    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
    ):
        self.session = session

    async def select_colab_creators(self, colab: tbls.ColabTable) -> list[tbls.ColabCreatorTable]:
        raw = await self.session.execute(
            sqlalchemy.select(tbls.ColabCreatorTable)
            .where(tbls.ColabCreatorTable.collabo_id == colab.collabo_id)
        )
        return [*raw.scalars().all()]

    async def create_data(
            self, notification: tbls.NotificationTable, notification_data_table: tbls.ColabTable
    ) -> NotificationData:
        creators = await self.select_colab_creators(notification_data_table)
        return ColabNotificationData(
            notification_type=NotificationType.COLAB,
            collabo_id=notification_data_table.collabo_id,
            owner_id=notification_data_table.owner_creator_id,
            title=notification_data_table.title,
            description=notification_data_table.description,
            creator_ids=[c.creator_id for c in creators],
        )

    def test_has_id(self, notification: tbls.NotificationTable) -> bool:
        return notification.collabo_id is not None

    def join_condition(self) -> ColumnElement[bool]:
        return tbls.ColabTable.collabo_id == tbls.NotificationTable.collabo_id

    def table(self) -> type[ColabTable]:
        return tbls.ColabTable


class ColabRequestNotificationDataType(NotificationDataType[tbls.ColabRequestTable]):

    async def create_data(
            self, notification: tbls.NotificationTable, notification_data_table: tbls.ColabRequestTable
    ) -> NotificationData:
        return ColabRequestNotificationData(
            notification_type=NotificationType.COLAB_REQUEST,
            from_creator_id=notification_data_table.sender_creator_id,
            colab_request_id=notification_data_table.collabo_request_id
        )

    def test_has_id(self, notification: tbls.NotificationTable) -> bool:
        return notification.collabo_request_id is not None

    def join_condition(self) -> ColumnElement[bool]:
        return tbls.ColabRequestTable.collabo_request_id == tbls.NotificationTable.collabo_request_id

    def table(self) -> type[tbls.ColabRequestTable]:
        return tbls.ColabRequestTable

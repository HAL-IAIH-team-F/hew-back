import dataclasses
import uuid

import sqlalchemy
from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class ColabApproveTable(BaseTable):
    __tablename__ = 'TBL_COLLABO_APPROVE'
    __table_args__ = (
        sqlalchemy.UniqueConstraint("colab_creator_id"),
    )

    collabo_approve_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    colab_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_COLLABO_CREATOR.collabo_creator_id'), nullable=False
    )

@dataclasses.dataclass
class ColabRequestTable(BaseTable):
    __tablename__ = 'TBL_COLLABO_REQUEST'

    collabo_request_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    sender_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False
    )
    receive_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False
    )

@dataclasses.dataclass
class ColabWantTable(BaseTable):
    __tablename__ = 'TBL_COLAB_WANT'

    colab_want_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    sender_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False
    )
    receive_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False
    )


@dataclasses.dataclass
class ColabTable(BaseTable):
    __tablename__ = 'TBL_COLLABO'

    collabo_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    owner_creator_id: Mapped[uuid.UUID] = Column(
        sqlalchemy.Uuid, ForeignKey('TBL_CREATOR.creator_id'), nullable=False
    )
    title: Mapped[str] = Column(sqlalchemy.String(64), nullable=False)
    description: Mapped[str] = Column(sqlalchemy.String(255), nullable=False)


@dataclasses.dataclass
class ColabCreatorTable(BaseTable):
    __tablename__ = 'TBL_COLLABO_CREATOR'
    __table_args__ = (
        sqlalchemy.UniqueConstraint("collabo_id","creator_id"),
    )

    collabo_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    collabo_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_COLLABO.collabo_id'), nullable=False
    )
    creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4
    )

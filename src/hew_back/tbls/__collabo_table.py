import dataclasses
import uuid

from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class CollaboTable(BaseTable):
    __tablename__ = 'TBL_COLLABO'

    collabo_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    sender_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4
    )
    receive_creator_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4
    )


@dataclasses.dataclass
class CollaboApproveTable(BaseTable):
    __tablename__ = 'TBL_COLLABO_APPROVE'

    approve_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4
    )
    collabo_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_COLLABO.collabo_id'), nullable=False
    )

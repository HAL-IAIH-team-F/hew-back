"""empty message

Revision ID: 22661e1abfd2
Revises: 419d48e5320f, 7402e6c7d71e
Create Date: 2024-11-15 14:37:42.787811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22661e1abfd2'
down_revision: Union[str, None] = ('419d48e5320f', '7402e6c7d71e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

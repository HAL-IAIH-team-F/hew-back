"""empty message

Revision ID: 64ff91ffb65c
Revises: cac1fe43e0ae, fec742e30493
Create Date: 2024-11-29 03:09:24.106715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64ff91ffb65c'
down_revision: Union[str, None] = ('cac1fe43e0ae', 'fec742e30493')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

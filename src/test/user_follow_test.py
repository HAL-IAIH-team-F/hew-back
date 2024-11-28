import uuid

import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import tbls, mdls, ENV
from test.conftest import session



@pytest_asyncio.fixture
async def user_table_saved(session) -> tbls.UserTable:
    table = tbls.UserTable.insert(
        session,
        user_id=,
    )
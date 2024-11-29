import uuid

import pytest
import pytest_asyncio
import datetime

from hew_back import tbls
from test.conftest import session, login_user_deps

from pydantic import BaseModel

# ユーザーデータ(creator_idと紐づかせるため,creatorテーブルにattributeでuser_idがある)
@pytest_asyncio.fixture
async def user_table_saved(session) -> tbls.UserTable:
    user_id = uuid.UUID("ff09e9a4-a9cc-4527-be60-d0a546141acf")
    table = tbls.UserTable(
        user_id=user_id,
        user_name="石破総理",
        user_screen_id="df53a6d2-88ea-46da-b030-b493214578bb", # ← スキーマをuuidにするべき
        user_icon_uuid=uuid.UUID("ea133ffa-d2be-4d9e-bfd0-1ed406f171cd"),
        user_date=datetime.datetime(2024, 11, 29 ,1,36,5,0),
        user_mail="Ishiba@gmail.com",
    )
    session.add(table)
    await session.commit()
    await session.refresh(table)
    return table

# クリエイターデータ
@pytest_asyncio.fixture
async def creator_saved(session, user_table_saved) -> tbls.CreatorTable:
    creator_id = uuid.UUID("13d324a1-4c98-4e47-8f8e-c00978598cdd")
    table = tbls.CreatorTable(
        creator_id=creator_id,
        user_id=user_table_saved.user_id,
        contact_address="@Ishiba",
        transfer_target="かぶあんど",
    )
    session.add(table)
    await session.commit()
    await session.refresh(table)
    return table

class UserFollowRequest(BaseModel):
    creator_id: uuid.UUID

@pytest.mark.asyncio
async def test_user_follow(
        client,
        session,
        login_access_token,
        login_user_deps,
        creator_saved
):

    body = UserFollowRequest(creator_id=creator_saved.creator_id)

    response = await client.post(
        path="api/user_follow",
        token=login_access_token.token,
        json_data=body
    )
    assert response.status_code == 200
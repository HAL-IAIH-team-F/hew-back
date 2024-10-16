import uuid
from datetime import datetime

import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import responses, tables
from test.conftest import session


#
# @pytest.fixture
# def post_user_body(session) -> bodies.PostUserBody:
#     return bodies.PostUserBody(
#         user_name="PostUserBody_user_name",
#         user_icon_uuid=None,
#     )
#
#
# @pytest_asyncio.fixture
# async def post_user_body_saved(session, keycloak_user_profile) -> bodies.PostUserBody:
#     body = bodies.PostUserBody(
#         user_name="PostUserBody_user_name_saved",
#         user_icon_uuid=None,
#     )
#     await body.save_new(session, keycloak_user_profile)
#     return body
@pytest_asyncio.fixture
async def product_table_saved(session, keycloak_user_profile) -> tables.ProductTable:
    table = tables.ProductTable.insert(
        session,
        product_price=100,
        product_title="title",
        product_text="text",
        product_date=datetime.now(),
        product_contents_uuid=uuid.uuid4(),
        product_thumbnail_uuid=uuid.uuid4(),
    )
    await session.commit()
    await session.refresh(table)
    return table


#
# @pytest.mark.asyncio
# async def test_create_user(session, client, token_info, post_user_body):
#     result = await client.post(
#         "/api/user",
#         post_user_body,
#         token_info.token
#     )
#     assert result.status_code == 200, f"invalid status code {result.json()}"
#     body = result.json()
#     assert body is not None
#     body = responses.SelfUserRes(**body)
#     result = await session.execute(
#         sqlalchemy.select(sqlalchemy.func.count())
#         .select_from(tables.UserTable)
#         .where(tables.UserTable.user_id == body.user_id)
#     )
#     assert result.scalar_one() == 1, f"\n{body}\n"
#
#
# @pytest.mark.asyncio
# async def test_get_self(client, token_info, session, post_user_body_saved, keycloak_user_profile):
#     result = await client.get(
#         "/api/user/self",
#         token_info.token
#     )
#     assert result.status_code == 200, f"invalid status code {result.read()}"
#     body = result.json()
#     assert body is not None
#     body = responses.SelfUserRes(**body)
#     assert body.user_id == keycloak_user_profile.sub
#     assert body.user_mail == keycloak_user_profile.email
#     assert body.user_name == post_user_body_saved.user_name

@pytest.mark.asyncio
async def test_read_products(client, session,product_table_saved):
    result = await client.get(
        "/products"
    )
    assert result.status_code == 200, f"invalid status code {result.read()}"
    body = result.json()
    assert body is not None
    records = await session.execute(
        sqlalchemy.select(tables.ProductTable).where()
    )
    records = records.scalars().all()
    assert len(records) == len(body)

    for i in range(len(records)):
        record = records[i]
        product = responses.GetProductsResponse(**body[i])

        assert record.product_id == product.product_id
        assert record.product_date == product.product_date
        assert record.product_text == product.product_text
        assert record.product_title == product.product_title
        assert record.product_price == product.product_price


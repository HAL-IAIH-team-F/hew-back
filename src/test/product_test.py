import uuid
from datetime import datetime, tzinfo, timezone

import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import tbls
from hew_back.product.__body import PostProductBody
from hew_back.product.__res import GetProductsResponse, ProductRes
from test.conftest import session


@pytest_asyncio.fixture
async def product_table_saved(session) -> tbls.ProductTable:
    table = tbls.ProductTable.insert(
        session,
        product_price=100,
        product_title="title",
        product_description="text",
        purchase_date=datetime.now(),
        product_contents_uuid=uuid.uuid4(),
        product_thumbnail_uuid=uuid.uuid4(),
    )
    await session.commit()
    await session.refresh(table)
    return table


@pytest.fixture
def post_product_body(session) -> PostProductBody:
    return PostProductBody(
        price=1,
        product_title="",
        product_description="",
        purchase_date=datetime(2024, 11, 20, 6, 38, 10, 656199).astimezone(timezone.utc),
        product_thumbnail_uuid=uuid.UUID('0ac01606-a086-47b2-acab-c9cda7dc3bb9'),
        product_contents_uuid=uuid.UUID('44f4ef3e-d667-4f0f-9fa4-bc13bb1fd98a'),
    )


@pytest.mark.asyncio
async def test_post_product(
        session,
        client,
        login_access_token,
        login_user,
        post_product_body,
        login_creator,
):
    response = await client.post(
        "/api/product",
        post_product_body,
        login_access_token.token
    )
    assert response.status_code == 200, f"invalid status code {response.json()}"
    body = response.json()
    assert body is not None
    res = ProductRes(**body)

    record = await session.execute(
        sqlalchemy.select(tbls.ProductTable)
        .where(tbls.ProductTable.product_id == res.product_id)
    )
    product_table: tbls.ProductTable = record.scalar_one()
    assert post_product_body.product_title == product_table.product_title
    assert post_product_body.product_description == product_table.product_description
    assert post_product_body.purchase_date == product_table.purchase_date
    assert post_product_body.product_thumbnail_uuid == product_table.product_thumbnail_uuid
    assert post_product_body.product_contents_uuid == product_table.product_contents_uuid

    record = await session.execute(
        sqlalchemy.select(tbls.CreatorProductTable)
        .where(tbls.CreatorProductTable.product_id == res.product_id)
    )
    creator_product_table: tbls.CreatorProductTable = record.scalar_one()
    await login_creator.refresh(session)
    assert login_creator.creator.creator_id == creator_product_table.creator_id


@pytest.mark.asyncio
async def test_read_products(client, session, product_table_saved):
    result = await client.get(
        "/api/products"
    )
    assert result.status_code == 200, f"invalid status code {result.read()}"
    body = result.json()
    assert body is not None
    records = await session.execute(
        sqlalchemy.select(tbls.ProductTable).where()
    )
    records = records.scalars().all()
    assert len(records) == len(body)

    for i in range(len(records)):
        record = records[i]
        product = GetProductsResponse(**body[i])

        assert record.product_id == product.product_id
        assert record.purchase_date == product.purchase_date
        assert record.product_description == product.product_description
        assert record.product_title == product.product_title
        assert record.product_price == product.product_price

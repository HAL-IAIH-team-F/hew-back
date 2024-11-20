import uuid
from datetime import datetime

import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import tbls
from hew_back.product.__res import GetProductsResponse
from test.conftest import session


@pytest_asyncio.fixture
async def product_table_saved(session) -> tbls.ProductTable:
    table = tbls.ProductTable.insert(
        session,
        product_price=100,
        product_title="title",
        product_description="text",
        listing_date=datetime.now(),
        product_contents_uuid=uuid.uuid4(),
        product_thumbnail_uuid=uuid.uuid4(),
    )
    await session.commit()
    await session.refresh(table)
    return table


@pytest.mark.asyncio
async def test_read_products(client, session, product_table_saved):
    result = await client.get(
        "/products"
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
        assert record.listing_date == product.product_date
        assert record.product_description == product.product_description
        assert record.product_title == product.product_title
        assert record.product_price == product.product_price

import pytest_asyncio
import sqlalchemy

from hew_back import tables, bodies, responses
from test.conftest import session

@pytest_asyncio.fixture
async def test_product_product_cart(session):
    result = await tables.ProductCartTable.get(
        "/product_cart",
        session,
    )
    print(result)
    # assert result.status_code == 200,

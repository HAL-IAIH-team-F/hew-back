import pytest_asyncio
import sqlalchemy

from hew_back import tables, bodies, responses, deps
from test.conftest import session

@pytest_asyncio.fixture
async def test_product_product_cart(session, user_deps):
    result = await tables.ProductCartTable.get_product_cart(
        "/product_cart",
        session,
        user_deps,
    )

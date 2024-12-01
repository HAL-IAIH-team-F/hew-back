import uuid
from datetime import datetime

import pytest
import pytest_asyncio

from hew_back.tbls import CartTable, CartProductTable, ProductTable
from test.conftest import session, login_keycloak_profile, login_user_deps


# 商品データ
@pytest_asyncio.fixture
async def mock_product(session) -> ProductTable:
    product_id = uuid.UUID("835dc2fd-127d-45d1-9a10-8002280777d8")
    product = ProductTable(
        product_id=product_id,
        product_price=300,
        product_title="缶バッジ",
        product_description="ランダムで全20種類",
        purchase_date=datetime(2024, 11, 9, 23, 15, 34),
        product_contents_uuid=uuid.UUID("3c4b6ab2-b82f-3cad-0cf4-a3a6612b7236"),
        product_thumbnail_uuid=uuid.UUID("0325de47-2abe-d6d9-e99e-da1a0c3c1f3e"),
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


#  -> GetProductsResponse

# refreshは → データ取り出し
# flushは非同期じゃないと、できない
# add →　commit
# add →　flush
# commitするならflushは不要

# カートデータ
@pytest_asyncio.fixture
async def mock_cart(session, login_keycloak_profile) -> CartTable:
    cart_id = uuid.UUID("3a5bfd4a-a2cb-8914-d0df-a139c5176f85")
    user_id = login_keycloak_profile.sub
    print(f"user_id→→→{user_id}")

    cart = CartTable(
        cart_id=cart_id,
        user_id=user_id,
        purchase_date=None
    )
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    return cart


# カートプロダクトデータ
@pytest_asyncio.fixture
async def create_mock_cart_product(session, mock_cart, mock_product) -> CartProductTable:
    await session.refresh(mock_cart)
    await session.refresh(mock_product)
    cart_product = CartProductTable(
        cart_id=mock_cart.cart_id,
        product_id=mock_product.product_id,
    )
    session.add(cart_product)
    await session.commit()
    await session.refresh(cart_product)
    return cart_product


@pytest_asyncio.fixture
async def mock_data(session, mock_product, mock_cart, create_mock_cart_product):
    await session.refresh(mock_product)
    await session.refresh(mock_cart)
    await session.refresh(create_mock_cart_product)

    return mock_product, mock_cart, create_mock_cart_product


@pytest.fixture
def cart_product_mock():
    product_id = uuid.UUID("a94cf31c-1e14-4189-9869-d1a455fb6529")
    product_contents = uuid.UUID("31fa694d-f5fa-4e75-880c-9bce43bfbe39")
    product_thumbnail = uuid.UUID("ee3cb623-15a0-487b-960a-7a23f6e9fea9")
    return ProductTable(
        product_id=product_id,
        product_price=1000,
        product_title="Test Product",
        product_description="This is a test product.",
        purchase_date=datetime(2022, 12, 9, 23, 15, 34),
        product_contents_uuid=product_contents,
        product_thumbnail_uuid=product_thumbnail,
    )


@pytest.mark.asyncio
async def test_read_product_cart(
        client,
        session,
        login_access_token,
        login_user_deps,
        mock_data
):
    # 非同期的にGETリクエストを送信
    response = await client.get(
        "/api/product_cart",
        login_access_token.token
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, {response.json()}"

    # レスポンスデータ 検証
    data = response.json()
    print(f"data----->{data}")

    # データがリストであることを確認
    assert isinstance(data, list), "レスポンスデータはリストではありません"

    # リストの中身が辞書であることを確認
    assert isinstance(data[0], dict), "レスポンスデータの要素は辞書ではありません"

    # 値の型 確認
    assert isinstance(data[0]['product_id'], str)
    assert isinstance(data[0]['product_price'], int)
    assert isinstance(data[0]['product_title'], str)
    assert isinstance(data[0]['product_description'], str)
    assert isinstance(data[0]['purchase_date'], str)
    assert isinstance(data[0]['product_contents_uuid'], str)
    assert isinstance(data[0]['product_thumbnail_uuid'], str)

    # 値の正確性を確認（価格の値範囲チェック）
    assert data[0]['product_price'] > 0, "product_priceが0以下です"


@pytest.mark.asyncio
async def test_cart_buy(
        client,
        session,
        login_access_token,
        login_user_deps,
        cart_product_mock
):
    response = await client.put(
        path="/api/cart_buy",
        token=login_access_token.token,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

    # tbls.CartProductに書いてある場所をProductaに移動させて、その関数をfixtureに書く
    # returnされる型を明示的にする

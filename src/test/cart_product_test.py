import uuid


import pytest

import pytest_asyncio

from hew_back import responses
from hew_back.tbls import UserTable, CartTable, CartProductTable, ProductTable
from test.conftest import session

from datetime import datetime

@pytest_asyncio.fixture
async def mock_data(session):

    # ユーザーデータ
    user_id = uuid.UUID("d89c7adb-74b2-f904-322e-70f642ee8132")
    user = UserTable(
        user_id=user_id,
        user_name="Ado",
        user_screen_id="d89c7adb-74b2-f904-322e-70f642ee8132",
        user_icon_uuid=uuid.UUID("0325de47-2abe-d6d9-e99e-da1a0c3c1f3e"),
        user_date=datetime(2024,11,9,22,15, 34),
        user_mail="Ado",
    )
    session.add(user)
    await session.flush()

    # 商品データ
    product_id = uuid.UUID("3a5bfd4a-a2cb-8914-d0df-a139c5176f85")
    products = ProductTable(
        product_id=product_id,
        product_price=300,
        product_title="缶バッジ",
        product_text="ランダムで全20種類",
        product_date=datetime(2024,11,9,23,15, 34),
        product_contents_uuid=uuid.UUID("3c4b6ab2-b82f-3cad-0cf4-a3a6612b7236"),
        product_thumbnail_uuid=uuid.UUID("0325de47-2abe-d6d9-e99e-da1a0c3c1f3e"),
    )
    session.add(products)
    await session.flush()

    # カートデータ
    cart_id = uuid.UUID("3a5bfd4a-a2cb-8914-d0df-a139c5176f85")
    cart = CartTable(
        cart_id=cart_id,
        user_id=user_id,
        purchase_date=None
    )
    session.add(cart)
    await session.flush()

    # カートプロダクトデータを作成
    cart_product = CartProductTable(
        cart_id=cart_id,
        product_id=product_id,
    )
    session.add(cart_product)

    await session.commit()
    await session.refresh(user)
    await session.refresh(cart)
    await session.refresh(products)
    await session.refresh(cart_product)


    return user, cart, products, cart_product

@pytest_asyncio.fixture
async  def cart_product_result(
        session,
        mock_data
    ):
    user, products, cart, cart_product = mock_data
    # print(f"user→{user} products→{products} cart→{cart} cart_product{cart_product}\n")
    print(f"user_id→→→{user.user_id}")
    result = await responses.CartProduct.get_cart_product(session=session, user_id=user.user_id)
    print(f"result→{result}")
    return [to_dict(item) for item in result]

def to_dict(instance):
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

@pytest.mark.asyncio
async def test_read_cart_product(
    client,
    # session,
    token_info,
    cart_product_result
):


    print(f"token_info--->{token_info},token_info.token--->{token_info.token}")
    # print(f"これがtoken_info------------------>{token_info}")

    # import jwt
    # class ENV:
    #     class token:
    #         secret_key = "secret"

    #     class db:
    #         host = "hew"
    #         port = 5433
    #         username = "postgres"
    #         password = "postgres"
    #
    # # シークレットキーはデコードに必要です
    # secret_key = ENV.token.secret_key
    #
    # # JWT トークンをデコードしてペイロードを取得
    # decoded_token = jwt.decode(token_info.token, secret_key, algorithms=["HS256"])
    #
    # # ペイロードから `sub` にアクセス
    # user_id = decoded_token["profile"]["sub"]
    # print(f"これがuser_id--------------------->{user_id}")

    # ユーザーが存在するか確認
    # user = await session.get(UserTable, user_id)
    # assert user is not None, "Userは存在しません！！！！！！！！！！！！！！！！！！！！！！！！！！！！"

    # 非同期的にGETリクエストを送信
    response = await client.get(
        "/cart_product",
        token_info.token
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, {response.json()}"
    # assert response.json() == cart_product_result, f"Unexpected response: {response.json()}"
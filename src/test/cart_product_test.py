import pytest_asyncio

import pytest

from sqlalchemy import true
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tables, bodies, responses, deps
from hew_back.responses import CartProduct
from test.conftest import session





from typing import Union

# テスト検証として、
# ダミーデータを渡してあげて、それが返ってくるか？


# フィクスチャは認証テストケースを補助するためのもので、直接テストを行わない
# なので、先頭に_testはつけない
@pytest.mark.asyncio
async def test_read_cart_product(client, session: AsyncSession, token_info):
    # トークンをデコードしてペイロードから `sub` を取得
    payload = jwt.decode(token_info.token, ENV.token.secret_key, algorithms=["HS256"])
    user_id = payload.get("profile", {}).get("sub")

    print(f"user_id: {user_id}")  # `sub` が正しく取得できたか確認

    # 認証ヘッダーを含めてリクエストを送信
    result = await client.get("/cart_product", headers={"Authorization": f"Bearer {token_info.token}"})

    assert result.status_code == 200, f"invalid status code: {result.status_code}"

    cart_product = await responses.CartProduct.get_cart_product(session=session, user_id=user_id)
    assert cart_product is not None, "cart product should not be None"


#    sub_value = token_info.jwt_token_data.profile.sub
#    email_verified_value = token_info.jwt_token_data.profile.email_verified
#    preferred_username = token_info.jwt_token_data.profile.preferred_username
#    email = token_info.jwt_token_data.profile.email
#   "token_type": "access", #   "exp": 1730376567は渡さなくていいの？


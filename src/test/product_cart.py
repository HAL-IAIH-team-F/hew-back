import pytest_asyncio

from sqlalchemy import true
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tables, bodies, responses, deps
from test.conftest import session


### すみません途中です！やり方分かったらなんとかします。

# テスト検証として、
# ダミーデータを渡してあげて、それが返ってくるか？


# フィクスチャは認証テストケースを補助するためのもので、直接テストを行わない
# なので、先頭に_testはつけない
@pytest_asyncio.fixture
async def read_product_curt(session: AsyncSession, token_info)-> responses.GetProductCart:
    body = responses.GetProductsResponse(
        product_text = "ください",
        product_id = "5250dec4-6978-2f7d-5264-afecbf53b4f5",
        product_thumbnail_uuid = "11a7c9dd-bc27-f574-e2a1-174cb07bde9e",
        product_price =23,
        product_title="かよちんの汗",
        product_date="2024-10-19T20:50:23",
        product_contents_uuid="a8c5ed68-ff1f-8c10-97b7-c814531ef852"
    )
    await responses. # セーブして
    return responses.GetProductCart.get_product_cart()

#    sub_value = token_info.jwt_token_data.profile.sub
#    email_verified_value = token_info.jwt_token_data.profile.email_verified
#    preferred_username = token_info.jwt_token_data.profile.preferred_username
#    email = token_info.jwt_token_data.profile.email
#   "token_type": "access", #   "exp": 1730376567は渡さなくていいの？


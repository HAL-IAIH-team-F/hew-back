import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, deps

from hew_back.chat.__result import MessageResult, ChatMessagesResult

class RecommendGet:
    @staticmethod
    async def get_recommend(
            product_id: uuid.UUID,
            session: AsyncSession,
            user: deps.UserDeps
    ) -> RecommendResult:
        recommend = await tbls.ProductTable.get_recommend(product_id, session, user)




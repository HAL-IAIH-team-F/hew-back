from hew_back import tbls, deps
from .__token_body import *
from .__user_body import *


class PostCreatorBody(BaseModel):
    user_id: uuid.UUID
    contact_address: str
    transfer_target: str

    async def save_new(self, user: deps.UserDeps, session: AsyncSession) -> results.CreatorResult:
        creator_table = tbls.CreatorTable.create(user.user_table, self.contact_address, self.transfer_target)
        creator_table.save_new(session)
        await session.commit()
        await session.refresh(creator_table)
        return results.CreatorResult(
            creator_table
        )


class PostChatBody(BaseModel):
    users: list[uuid.UUID]

    async def save_new(self, user: deps.UserDeps, session: AsyncSession) -> results.ChatUsersResult:
        users = tbls.UserTable.find_all(session, self.users)

        chat = tbls.ChatTable.create(session)
        await session.commit()
        await session.refresh(chat)
        users = await  users
        users.append(user.user_table)
        for user in users:
            await session.refresh(user)

        users = tbls.ChatUserTable.create_all(chat, users, session)
        await session.commit()
        for user in users:
            await session.refresh(user)
        await session.refresh(chat)

        return results.ChatUsersResult(
            chat, users
        )


class PostChatMessageBody(BaseModel):
    message: str
    images: list[uuid.UUID]

    async def save_new(self, session: AsyncSession, chat_id: uuid.UUID) -> results.ChatMessageResult:
        chat = await tbls.ChatTable.find(session, chat_id)

        last_index = await tbls.ChatMessageTable.last_index(session, chat)
        chat_message = tbls.ChatMessageTable.create(session, chat, last_index + 1, self.message)
        await session.flush()
        await session.refresh(chat_message)
        images = tbls.ChatImageTable.create_all(chat, self.images, session)
        await session.flush()
        for image in images:
            await session.refresh(image)

        return results.ChatMessageResult(
            chat, chat_message, images
        )

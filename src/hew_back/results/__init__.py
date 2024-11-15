import uuid
from dataclasses import dataclass

from .. import tbls, reses


@dataclass
class CreatorResult:
    creator: tbls.CreatorTable

    def to_creator_res(self):
        return reses.CreatorResponse.create(
            creator_id=self.creator.creator_id,
            user_id=self.creator.user_id,
            contact_address=self.creator.contact_address,
            transfer_target=self.creator.transfer_target,
        )


@dataclass
class UserResult:
    user: tbls.UserTable

    def to_self_user_res(self):
        return reses.SelfUserRes.create_by_user_table(self.user)


@dataclass
class ChatUsersResult:
    chat: tbls.ChatTable
    users: list[tbls.ChatUserTable]

    def to_chat_res(self):
        user_ids: list[uuid.UUID] = []
        for chat_user in self.users:
            user_ids.append(chat_user.user_id)
        return reses.ChatRes.create(self.chat.chat_id, user_ids)


@dataclass
class FindChatsResult:
    chats: list[ChatUsersResult]

    def to_chat_reses(self) -> list[reses.ChatRes]:
        result: list[reses.ChatRes] = []
        for chat in self.chats:
            result.append(chat.to_chat_res())
        return result

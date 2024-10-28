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
class ChatSaveNewResult:
    chat: tbls.ChatTable
    users: list[tbls.ChatUserTable]


@dataclass
class FindChatsResult:
    chats: list[tbls.ChatTable]

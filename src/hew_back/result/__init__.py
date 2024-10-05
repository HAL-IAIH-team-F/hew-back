from dataclasses import dataclass

from .. import tables, responses


@dataclass
class CreatorModel:
    creator: tables.CreatorTable


@dataclass
class UserModel:
    user: tables.UserTable

    def to_self_user_res(self):
        return responses.SelfUserRes.create_by_user_table(self.user)

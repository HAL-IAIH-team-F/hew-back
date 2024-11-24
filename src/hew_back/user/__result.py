import dataclasses

from hew_back import tbls
from hew_back.user.__res import SelfUserRes


@dataclasses.dataclass
class UserResult:
    user: tbls.UserTable

    def to_self_user_res(self):
        return SelfUserRes.create_by_user_table(self.user)

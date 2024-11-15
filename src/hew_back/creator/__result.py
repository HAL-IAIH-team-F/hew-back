from dataclasses import dataclass

from hew_back import tbls
from hew_back.creator.__res import CreatorResponse


@dataclass
class CreatorResult:
    creator: tbls.CreatorTable

    def to_creator_res(self):
        return CreatorResponse.create(
            creator_id=self.creator.creator_id,
            user_id=self.creator.user_id,
            contact_address=self.creator.contact_address,
            transfer_target=self.creator.transfer_target,
        )

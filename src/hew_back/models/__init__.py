from dataclasses import dataclass

from .__token import *

@dataclass
class CreatorModel:
    creator: tbls.CreatorTable

import dataclasses

from .__orderdirection import *


@dataclasses.dataclass
class Pair[A, B]:
    first: A
    second: B

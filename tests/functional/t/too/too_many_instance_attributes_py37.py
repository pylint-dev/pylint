# pylint: disable=missing-docstring, too-few-public-methods
from dataclasses import dataclass, InitVar

# InitVars should not count as instance attributes (see issue #3754)
# Default max_instance_attributes is 7
@dataclass
class Hello:
    a_1: int
    a_2: int
    a_3: int
    a_4: int
    a_5: int
    a_6: int
    a_7: int
    a_8: InitVar[int]

    def __post_init__(self, a_8):
        self.a_1 += a_8

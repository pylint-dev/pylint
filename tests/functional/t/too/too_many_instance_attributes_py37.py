"""
InitVars should not count as instance attributes (see issue #3754)
Default max_instance_attributes is 7
"""

# pylint: disable=missing-docstring, too-few-public-methods

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from dataclasses import dataclass, InitVar


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

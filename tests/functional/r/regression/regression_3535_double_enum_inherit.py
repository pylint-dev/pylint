# pylint: disable=missing-docstring,invalid-name

import enum

class A(enum.Enum):
    pass

class B(A):
    x = enum.auto()

print(B.__members__['x'])

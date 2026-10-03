# pylint: disable=missing-docstring,invalid-name
# https://github.com/pylint-dev/pylint/issues/3535

import enum

class A(enum.Enum):
    pass

class B(A):
    x = enum.auto()

print(B.__members__['x'])

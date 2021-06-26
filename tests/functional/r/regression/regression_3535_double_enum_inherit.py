# pylint: disable=missing-docstring,invalid-name
# https://github.com/PyCQA/pylint/issues/3535

import enum

class A(enum.Enum):
    pass

class B(A):
    x = enum.auto()

print(B.__members__['x'])

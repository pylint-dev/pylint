"""Tests for dataclass attributes with basic type annotations.

Tests for regressions from https://github.com/pylint-dev/astroid/pull/1126
"""

# pylint: disable=missing-docstring,too-few-public-methods,pointless-statement,redefined-builtin, fixme

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


class Dummy:
    pass


@dataclass
class MyClass:
    # Attribute inference does not support Optional, so Uninferable is yielded
    # This should not trigger any type errors from pylint
    attr0: Optional[Dummy]

    attr1: int
    attr2: str
    attr3: Callable[[int], int]
    attr4: List[int]
    attr5: Dict[str, str]


OBJ = MyClass(None, 1, 'hi', lambda x: x, [], {})

LIST = [0, 1, 2]
print(LIST[OBJ.attr0])
print(LIST[OBJ.attr1])
print(LIST[OBJ.attr2])  # [invalid-sequence-index]

print(LIST[OBJ.attr0::])
print(LIST[OBJ.attr1::])
print(LIST[OBJ.attr2::])  # [invalid-slice-index]

OBJ.attr0(100)
OBJ.attr1(100)  # [not-callable]
OBJ.attr3(100)

print(-OBJ.attr0)
print(-OBJ.attr1)
print(-OBJ.attr2)  # [invalid-unary-operand-type]

print(1 + OBJ.attr0)
print(1 + OBJ.attr1)
print(1 + OBJ.attr2)  # Should be an error here once unsupported-binary-operation is enabled

print(1 in OBJ.attr0)
print(1 in OBJ.attr1)  # [unsupported-membership-test]
print(1 in OBJ.attr4)
print('hi' in OBJ.attr5)

print(OBJ.attr0[1])
print(OBJ.attr1[1])  # [unsubscriptable-object]
print(OBJ.attr4[1])
print(OBJ.attr5['hi'])

OBJ.attr0[1] = 1
OBJ.attr1[1] = 1  # [unsupported-assignment-operation]
OBJ.attr4[1] = 1
OBJ.attr5['hi'] = 'bye'

del OBJ.attr0[1]
del OBJ.attr1[1]  # [unsupported-delete-operation]
del OBJ.attr4[1]
del OBJ.attr5['hi']


class Manager:
    def __enter__(self):
        pass

    def __exit__(self, type_, value, traceback):
        pass


@dataclass
class MyClass2:
    attr0: Optional[Dummy]
    attr1: Manager
    attr2: str


OBJ2 = MyClass2(None, Manager(), 'hi')
with OBJ2.attr0:
    pass
with OBJ2.attr1:
    pass
with OBJ2.attr2:  # [not-context-manager]
    pass


class Test1(metaclass=OBJ.attr0):
    pass


class Test2(metaclass=OBJ.attr1):  # [invalid-metaclass]
    pass


{}[OBJ.attr0] = 1
{}[OBJ.attr1] = 1
{}[OBJ.attr5] = 1  # [unhashable-member]

for k, v in OBJ.attr5:  # TODO: Should be a dict-iter-missing-items error
    print(k, v)

__name__ = OBJ.attr0
__name__ = OBJ.attr1  # TODO: Should be a non-str-assignment-to-dunder-name error
__name__ = OBJ.attr2

print(isinstance(1, OBJ.attr0))
print(isinstance(1, OBJ.attr1))  # [isinstance-second-argument-not-valid-type]

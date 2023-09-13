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


obj = MyClass(None, 1, 'hi', lambda x: x, [], {})

lst = [0, 1, 2]
print(lst[obj.attr0])
print(lst[obj.attr1])
print(lst[obj.attr2])  # [invalid-sequence-index]

print(lst[obj.attr0::])
print(lst[obj.attr1::])
print(lst[obj.attr2::])  # [invalid-slice-index]

obj.attr0(100)
obj.attr1(100)  # [not-callable]
obj.attr3(100)

print(-obj.attr0)
print(-obj.attr1)
print(-obj.attr2)  # [invalid-unary-operand-type]

print(1 + obj.attr0)
print(1 + obj.attr1)
print(1 + obj.attr2)  # Should be an error here once unsupported-binary-operation is enabled

print(1 in obj.attr0)
print(1 in obj.attr1)  # [unsupported-membership-test]
print(1 in obj.attr4)
print('hi' in obj.attr5)

print(obj.attr0[1])
print(obj.attr1[1])  # [unsubscriptable-object]
print(obj.attr4[1])
print(obj.attr5['hi'])

obj.attr0[1] = 1
obj.attr1[1] = 1  # [unsupported-assignment-operation]
obj.attr4[1] = 1
obj.attr5['hi'] = 'bye'

del obj.attr0[1]
del obj.attr1[1]  # [unsupported-delete-operation]
del obj.attr4[1]
del obj.attr5['hi']


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


obj2 = MyClass2(None, Manager(), 'hi')
with obj2.attr0:
    pass
with obj2.attr1:
    pass
with obj2.attr2:  # [not-context-manager]
    pass


class Test1(metaclass=obj.attr0):
    pass


class Test2(metaclass=obj.attr1):  # [invalid-metaclass]
    pass


{}[obj.attr0] = 1
{}[obj.attr1] = 1
{}[obj.attr5] = 1  # [unhashable-member]

for k, v in obj.attr5:  # TODO: Should be a dict-iter-missing-items error
    print(k, v)

__name__ = obj.attr0
__name__ = obj.attr1  # TODO: Should be a non-str-assignment-to-dunder-name error
__name__ = obj.attr2

print(isinstance(1, obj.attr0))
print(isinstance(1, obj.attr1))  # [isinstance-second-argument-not-valid-type]

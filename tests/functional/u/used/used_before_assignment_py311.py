"""assert_never() introduced in 3.11"""
from enum import Enum
from typing import assert_never


class MyEnum(Enum):
    """A lovely enum."""
    VAL1 = 1
    VAL2 = 2


def do_thing(val: MyEnum) -> None:
    """Do a thing."""
    if val is MyEnum.VAL1:
        note = 'got 1'
    elif val is MyEnum.VAL2:
        note = 'got 2'
    else:
        assert_never(val)

    print('Note:', note)

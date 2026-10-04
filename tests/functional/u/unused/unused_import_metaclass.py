"""Names used only in a ``metaclass=`` expression are used.

https://github.com/pylint-dev/pylint/issues/1630
"""
# pylint: disable=missing-docstring,too-few-public-methods,import-error

import sys
from abc import ABCMeta

import unknown
from unknown import BlockMeta, CallMeta, FunctionMeta, NestedMeta, make_meta


class InConditionalExpression(metaclass=ABCMeta if sys.version_info else type):
    pass


class InCallArgument(metaclass=make_meta(CallMeta)):
    pass


class Outer:
    class InClassBody(metaclass=NestedMeta):
        pass


if sys.platform != "win32":

    class InIfBlock(metaclass=BlockMeta):
        pass


def define_in_block(flag):
    if flag:

        class InFunctionBlock(metaclass=FunctionMeta):
            pass

        return InFunctionBlock
    return None


print(unknown)


def define_after_an_earlier_use():
    class UnknownMetaclass(metaclass=unknown.Meta):
        pass

    return UnknownMetaclass

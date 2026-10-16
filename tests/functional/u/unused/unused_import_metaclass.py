"""Names used only in a ``metaclass=`` expression are used.

https://github.com/pylint-dev/pylint/issues/1630
"""
# pylint: disable=missing-docstring,too-few-public-methods,import-error

import sys
from abc import ABCMeta
from enum import EnumMeta

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


def define_in_nested_scopes():
    # A lambda body and the first iterable of a comprehension are evaluated
    # in the scope enclosing the class.
    # pylint: disable-next=import-outside-toplevel
    from unknown import ComprehensionMeta, LambdaMeta, ParamMeta

    class InLambdaBody(metaclass=(lambda: LambdaMeta)()):
        pass

    class InComprehension(metaclass=[meta for meta in ComprehensionMeta][0]):
        pass

    class InLambdaArgument(metaclass=(lambda meta: meta)(ParamMeta)):
        pass

    return InLambdaBody, InComprehension, InLambdaArgument


Shadowed = ABCMeta


class Holder:
    ClassLevelMeta = ABCMeta
    Shadowed = type

    class InClassBody(metaclass=ClassLevelMeta):
        pass

    def method(self):
        # A class body is not visible from the functions defined in it.
        class InMethod(metaclass=ClassLevelMeta):  # [undefined-variable]
            pass

        class UsesModuleLevel(metaclass=Shadowed):
            pass

        return InMethod, UsesModuleLevel


class Other:
    ClassLevelMeta = ABCMeta
    EnumMeta = type

    # A class body is not visible from the body of a lambda either.
    class InLambdaInClassBody(metaclass=(lambda: ClassLevelMeta)()):  # [undefined-variable]
        pass

    def method(self):
        # Uses the import, not the class attribute shadowing it.
        class UsesImport(metaclass=EnumMeta):
            pass

        return UsesImport

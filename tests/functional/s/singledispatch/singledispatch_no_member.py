"""Tests for no-member false positives on functools.singledispatch calls.

https://github.com/pylint-dev/pylint/issues/2647
"""
# pylint: disable=missing-docstring,too-few-public-methods
from functools import singledispatch


class HasNoAttributeX:
    def __init__(self, not_attribute_x):
        self.not_attribute_x = not_attribute_x


class HasAttributeX:
    def __init__(self, attribute_x):
        self.attribute_x = attribute_x


@singledispatch
def example_singledispatch(argument):
    return argument


@example_singledispatch.register
def _(argument: HasNoAttributeX) -> HasAttributeX:
    return HasAttributeX(argument.not_attribute_x)


def via_intermediate_variable():
    argument = HasNoAttributeX(3)
    result = example_singledispatch(argument)

    # Statically, the generic function's body just returns its argument
    # unchanged, so an over-eager inference would assume `result` is still
    # a `HasNoAttributeX`. At runtime the registered overload for
    # `HasNoAttributeX` is dispatched instead, returning a `HasAttributeX`.
    assert result.attribute_x == 3


def via_direct_call():
    assert example_singledispatch(HasNoAttributeX(3)).attribute_x == 3


def real_no_member_bug_is_still_caught():
    # Unrelated to singledispatch: this must still be flagged.
    result = HasNoAttributeX(3)
    result.definitely_not_a_real_attribute()  # [no-member]

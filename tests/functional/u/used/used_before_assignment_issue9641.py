"""Regression test for https://github.com/pylint-dev/pylint/issues/9641
Walrus operator assignment in stacked decorators should not trigger used-before-assignment.
"""
# pylint: disable=missing-function-docstring


def dec(x):
    return x


@dec(l := [1, 2, 3])
@dec(l)
def test_func(x=l):
    return x


# Reversing the decorator order should still trigger used-before-assignment
@dec(undefined_order)  # [used-before-assignment]
@dec(undefined_order := 1)
def test_reversed(x=undefined_order):
    return x


# Self-reference in the walrus definition should still trigger used-before-assignment
@dec(self_ref := self_ref + 1)  # [used-before-assignment]
def test_self_reference(x=self_ref):
    return x

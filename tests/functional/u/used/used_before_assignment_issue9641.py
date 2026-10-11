"""Regression test for https://github.com/pylint-dev/pylint/issues/9641
Walrus operator assignment in stacked decorators should not trigger used-before-assignment.
"""
# pylint: disable=missing-function-docstring,unused-argument


def dec(*args):
    return lambda fn: fn


@dec("plain")
@dec(l := [1, 2, 3])
@dec(l)
def test_func(x=l):
    return x


# Reversing the decorator order should still trigger used-before-assignment
@dec(unrelated := 0)
@dec(undefined_order)  # [used-before-assignment]
@dec(undefined_order := 1)
def test_reversed(x=undefined_order):
    return x


# Self-reference in the walrus definition should still trigger used-before-assignment
@dec(self_ref := self_ref + 1)  # [used-before-assignment]
def test_self_reference(x=self_ref):
    return x


# Walrus target not defined in decorators falling back to later parameter default
@dec(undef_walrus)  # [used-before-assignment]
@dec(other_walrus := 1)
def test_fallback_to_args(x=(undef_walrus := 2)):
    return x


# Same-line walrus assignment before use should not trigger used-before-assignment
@dec(same_a := 1, same_a)
def test_same_line():
    pass


# Same-line walrus assignment after use should trigger used-before-assignment
@dec(same_b, same_b := 1)  # [used-before-assignment]
def test_same_line_reversed():
    pass

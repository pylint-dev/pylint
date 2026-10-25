"""Regression test for https://github.com/pylint-dev/pylint/issues/11647
False positive undefined-variable with := and blank type annotation in comprehension.
"""

# pylint: disable=missing-function-docstring,unreachable


def test_listcomp():
    x: int
    return [
        x
        # walrus defines x before element evaluation
        for i in range(2)
        if (x := i)
    ]


def test_setcomp():
    x: int
    return {
        x
        # walrus defines x before element evaluation
        for i in range(2)
        if (x := i)
    }


def test_dictcomp():
    x: int
    return {
        x: x
        # walrus defines x before element evaluation
        for i in range(2)
        if (x := i)
    }


def test_genexpr():
    x: int
    return (
        x
        # walrus defines x before element evaluation
        for i in range(2)
        if (x := i)
    )


def test_undefined_after():
    x: int
    return [
        x  # [undefined-variable]
        # not assigned in comprehension
        for i in range(2)
    ]
    x = 1


def test_reversed_filter():
    x: int
    return [
        (x := i)
        # filter runs before element walrus
        for i in range(2)
        if x  # [undefined-variable]
    ]


def test_nested_comp():
    x: int
    return [
        [x for _ in range(2)]
        # walrus defines x before element evaluation
        for i in range(2)
        if (x := i)
    ]


# The assignment expression can be skipped by a short-circuit, see
# https://github.com/pylint-dev/pylint/pull/11649#issuecomment-6137512443
# and https://github.com/pylint-dev/pylint/issues/8658 for the general case
def test_skipped_by_or(allow: bool):
    x: int
    return [
        x  # [undefined-variable]
        for i in range(2)
        if allow or (x := i)
    ]


def test_skipped_by_true_or():
    x: int
    return [
        x  # [undefined-variable]
        for i in range(2)
        if True or (x := i)  # pylint: disable=condition-evals-to-constant
    ]


def test_skipped_by_conditional_expression(allow: bool):
    x: int
    return [
        x  # [undefined-variable]
        for i in range(2)
        if ((x := i) if allow else i)
    ]


def test_skipped_by_and_then_or(allow: bool):
    x: int
    return [
        x  # [undefined-variable]
        for i in range(2)
        if (allow and (x := i)) or i
    ]


def test_after_and(allow: bool):
    x: int
    return [
        x
        for i in range(2)
        if allow and (x := i)
    ]


def test_first_in_or():
    x: int
    return [
        x
        for i in range(2)
        if (x := i) or i
    ]


# The assignment expression only runs before the element, not before
# the other conditions that come earlier in the comprehension
def test_read_in_earlier_filter():
    x: int
    return [
        i
        for i in range(2)
        if x  # [undefined-variable]
        if (x := i)
    ]


def test_read_earlier_in_same_filter():
    x: int
    return [
        i
        for i in range(2)
        if x  # [undefined-variable]
        and (x := i)
    ]


def test_read_in_filter_of_earlier_generator():
    x: int
    return [
        i
        for i in range(2)
        if x  # [undefined-variable]
        for j in range(2)
        if (x := j)
    ]

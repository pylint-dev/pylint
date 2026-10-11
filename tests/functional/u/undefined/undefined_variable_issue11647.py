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

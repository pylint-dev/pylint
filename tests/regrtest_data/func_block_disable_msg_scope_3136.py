# pylint: disable=missing-module-docstring,missing-function-docstring
"""Regression data for https://github.com/pylint-dev/pylint/issues/3136.

A block-scoped disable directive placed inside an ``if`` body must not leak
into sibling ``elif``/``else`` blocks of the same statement.
"""


def func(value):
    generator = (x for x in range(10))
    if value == 1:
        # pylint: disable=stop-iteration-return
        next(generator)
    elif value == 2:
        next(generator)
    else:
        next(generator)

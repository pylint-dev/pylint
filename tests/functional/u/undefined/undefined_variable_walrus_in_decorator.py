"""Regression test for https://github.com/pylint-dev/pylint/issues/5735.

A name bound by ``:=`` in the condition of a comprehension, inside a decorator
call, is defined for the rest of that comprehension.
"""

# pylint: disable=missing-function-docstring

DATA = ["abcdef", "qwerty"]


def preprocess(text):
    return text + "xyz"


def decorator(arg):
    print(arg)
    return lambda function: function


@decorator(
    [
        found.upper()
        for string in DATA
        if (found := preprocess(string)).startswith("abc") and "bcd" in found
    ],
)
def decorated():
    pass

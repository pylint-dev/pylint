"""Regression test for https://github.com/pylint-dev/pylint/issues/11491.

Inferring ``Class.__bases__`` used to crash the stdlib checker.
"""

# pylint: disable=missing-class-docstring, too-few-public-methods


class MyClass:
    pass


MyClass.__bases__()  # [not-callable]

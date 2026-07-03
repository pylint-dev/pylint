"""Test that positional only argument annotations are properly marked as consumed

https://github.com/pylint-dev/pylint/issues/3462
"""
from typing import AnyStr, Set


def func(arg: AnyStr, /, arg2: Set[str]):
    """Uses positional only arguments"""
    return arg, arg2

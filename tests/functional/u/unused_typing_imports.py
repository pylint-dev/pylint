# pylint: disable=missing-docstring, bad-whitespace
"""Regression test for https://github.com/PyCQA/pylint/issues/1168

The problem was that we weren't handling keyword-only arguments annotations,
which means we were never processing them.
"""

import re
import typing
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Pattern,
    Sequence,
    Set,
    Tuple,
)


def func1(arg: Optional[Callable]=None):
    return arg


def func2(*, arg: Optional[Iterable]=None):
    return arg


SOME_VALUE = [1] # type: List[Any]
for VALUE in [[1], [2], [3]]:  # type: Tuple[Any]
    print(VALUE)


class ContextManager:
    def __enter__(self):
        return {1}

    def __exit__(self, *_args):
        pass


with ContextManager() as SOME_DICT: # type: Set[int]
    print(SOME_DICT)


def func_test_type_comment(param):
    # type: (NamedTuple) -> Tuple[NamedTuple, Pattern]
    return param, re.compile('good')


def typing_fully_qualified():
    variable = None  # type: typing.Optional[str]
    other_variable: 'typing.Optional[str]' = None
    return variable, other_variable


def function(arg1,  # type: Iterable
             arg2  # type: List
            ):
    # type: (...) -> Sequence
    """docstring"""
    print(arg1, arg2)

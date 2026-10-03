"""Verify if call to function or method inside tests are missing parentheses."""
# pylint: disable=using-constant-test, missing-docstring
# pylint: disable=invalid-name, expression-not-assigned, unnecessary-lambda-assignment

import os


import collections
import random

try:
    import multiprocessing
    from multiprocessing import synchronize  # noqa pylint: disable=unused-import
except ImportError:
    multiprocessing = None  # type: ignore[assignment]


def bool_function():
    return True


def nonbool_function():
    return 42


class Class:
    @staticmethod
    def bool_method():
        return False

    @staticmethod
    def nonbool_method():
        return 42


if collections:
    pass

if bool_function:  # [missing-parentheses-for-call-in-test]
    pass

if not bool_function():
    pass

if nonbool_function:  # [missing-parentheses-for-call-in-test]
    pass

if nonbool_function() != 42:
    pass

instance = Class()

if instance.bool_method:  # [missing-parentheses-for-call-in-test]
    pass

if not instance.bool_method():
    pass

if not instance.nonbool_method:
    pass
elif instance.bool_method:  # [missing-parentheses-for-call-in-test]
    pass

bool_lambda = lambda: True

if bool_lambda:  # [missing-parentheses-for-call-in-test]
    pass

if not bool_lambda():
    pass

nonbool_lambda = lambda: 42

if nonbool_lambda:  # [missing-parentheses-for-call-in-test]
    pass

if not nonbool_lambda():
    pass

MY_VALUE = 42 if bool_function else -1  # [missing-parentheses-for-call-in-test]
MY_2ND_VALUE = 42 if not bool_function() else -1
MY_THIRD_VALUE = 42 if bool_lambda else -1  # [missing-parentheses-for-call-in-test]
MY_FOURTH_VALUE = 42 if nonbool_lambda else -1  # [missing-parentheses-for-call-in-test]

[x for x in range(100) if bool_function]  # [missing-parentheses-for-call-in-test]
[x for x in range(100) if bool_lambda]  # [missing-parentheses-for-call-in-test]
[x for x in range(100) if not bool_function()]
[x for x in range(100) if not bool_lambda()]
[x for x in range(100) if nonbool_lambda]  # [missing-parentheses-for-call-in-test]
[x for x in range(100) if nonbool_function]  # [missing-parentheses-for-call-in-test]


def non_const_node_function():
    return (1, 2, 42)


if non_const_node_function:  # [missing-parentheses-for-call-in-test]
    pass


def yielding_function():
    yield 42


if yielding_function:  # [missing-parentheses-for-call-in-test]
    pass

if not yielding_function():
    pass


def is_it_a_good_day():
    """Seems like this is not working in python 3.11 ?"""
    return random.choice([True, False])


if is_it_a_good_day:  # [missing-parentheses-for-call-in-test]
    print("Today is a good day!")
elif yielding_function:  # [missing-parentheses-for-call-in-test]
    print("multiple condition")


def _cpu_count() -> int:
    """Reproducer for an inference error that can happen in
    missing-parentheses-for-call-in-test"""
    sched_getaffinity = getattr(os, "sched_getaffinity", None)
    if sched_getaffinity:
        print(sched_getaffinity)
    elif multiprocessing:
        multiprocessing.cpu_count()

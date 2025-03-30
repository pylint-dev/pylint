"""Tests for used-before-assignment when postponed evaluation of annotations is enabled"""
# pylint: disable=missing-function-docstring, invalid-name, missing-class-docstring, too-few-public-methods
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    var = 1
    import math

print(var)  # [used-before-assignment]

def function_one(m: math):  # no error for annotations
    return m

# https://github.com/pylint-dev/pylint/issues/8893
if TYPE_CHECKING:
    import datetime

def f():
    return datetime.datetime.now()  # [used-before-assignment]

def g() -> datetime.datetime:
    return datetime.datetime.now()  # [used-before-assignment]

if TYPE_CHECKING:
    class X:
        pass

def h():
    return X()  # [used-before-assignment]

def i() -> X:
    return X()  # [used-before-assignment]

if TYPE_CHECKING:
    from mod import Y

def j():
    return {Y() for _ in range(1)}  # FALSE NEGATIVE

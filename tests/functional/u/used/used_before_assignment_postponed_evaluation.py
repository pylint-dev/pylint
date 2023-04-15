"""Tests for used-before-assignment when postponed evaluation of annotations is enabled"""
# pylint: disable=missing-function-docstring, invalid-name
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    var = 1
    import math

print(var)  # [used-before-assignment]

def function_one(m: math):  # no error for annotations
    return m

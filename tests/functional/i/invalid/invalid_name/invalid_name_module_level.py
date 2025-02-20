"""Tests for invalid name for names declared at module level"""
# pylint: disable=missing-class-docstring, too-few-public-methods, missing-function-docstring

import collections

Class = collections.namedtuple("a", ("b", "c"))


class ClassA:
    pass


ClassB = ClassA


def A():  # [invalid-name]
    return 1, 2, 3


CONSTA, CONSTB, CONSTC = A()
CONSTD = A()

CONST = "12 34 ".rstrip().split()


ASSIGNMENT_THAT_CRASHED_PYLINT = type(float.__new__.__code__)


if CONST:
    OTHER_CONST = 1
else:
    OTHER_CONST = 2

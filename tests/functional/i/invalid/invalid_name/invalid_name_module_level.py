"""Tests for invalid name for names declared at module level"""
# pylint: disable=missing-class-docstring, too-few-public-methods, missing-function-docstring, wrong-import-position

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


# Exclusive assignment: uses const regex
if CONST:
    OTHER_CONST = 1
elif CONSTA:
    OTHER_CONST = 2
else:
    OTHER_CONST = 3


# Lists, sets, and objects can pass against the variable OR const regexes.
if CONST:
    other_const = [1]
elif CONSTA:
    other_const = [2]
else:
    other_const = [3]


from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    VERSION = version("ty")  # uninferable
except PackageNotFoundError:
    VERSION = "0.0.0"


from typing import Annotated
IntWithAnnotation = Annotated[int, "anything"]

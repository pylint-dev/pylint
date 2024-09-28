"""used-before-assignment re: python 3.12 generic typing syntax (PEP 695)"""

from typing import Callable
type Point[T] = tuple[T, ...]
type Alias[*Ts] = tuple[*Ts]
type Alias[**P] = Callable[P]

# pylint: disable = invalid-name, missing-class-docstring, too-few-public-methods

# https://github.com/pylint-dev/pylint/issues/9815
type IntOrX = int | X  # [used-before-assignment] FALSE POSITIVE

class X:
    pass

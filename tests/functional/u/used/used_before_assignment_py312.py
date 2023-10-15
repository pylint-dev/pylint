"""used-before-assignment re: python 3.12 generic typing syntax (PEP 695)"""

from typing import Callable
type Point[T] = tuple[T, ...]
type Alias[*Ts] = tuple[*Ts]
type Alias[**P] = Callable[P]

"""PEP 695 generic typing nodes"""

from collections.abc import Callable, Sequence

type Point[T] = tuple[T, ...]
type Point[t] = tuple[t, ...]  # [invalid-name]

# Don't report typevar-name-incorrect-variance for type parameter
# The variance is determined by the type checker
type Array[T_co] = Sequence[T_co]

type Call[**_P] = Callable[_P, None]
type Call[**p] = Callable[p, None]  # [invalid-name]

type Tpl[*_Ts] = tuple[_Ts]
type Tpl[*ts] = tuple[ts]  # [invalid-name]

"""PEP 695 generic typing nodes"""

from collections.abc import Sequence

type Point[T] = tuple[T, ...]
type Point[t] = tuple[t, ...]  # [invalid-name]

# Don't report typevar-name-incorrect-variance for type parameter
# The variance is determined by the type checker
type Array[T_co] = Sequence[T_co]

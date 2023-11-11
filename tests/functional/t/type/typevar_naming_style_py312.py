"""PEP 695 generic typing nodes"""

type Point[T] = tuple[T, ...]
type Point[t] = tuple[t, ...]  # [invalid-name]

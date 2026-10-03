"""PEP 695 generic typing nodes"""

type Point[T] = tuple[T, ...]
type point[T] = tuple[T, ...]  # [invalid-name]

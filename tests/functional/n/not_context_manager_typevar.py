"""A name bound by a ``type`` statement (a TypeVar) is not a context manager."""
# pylint: disable=missing-docstring

type Alias[T] = int

with T:  # [not-context-manager]
    pass

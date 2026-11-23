"""Abstract base classes from collections.abc are not counted as ancestors.

``STDLIB_CLASSES_IGNORE_ANCESTOR`` was transcribed from ``_collections_abc.__all__``
but ``Callable`` was left out, so it was the one ABC in that module that still
counted towards ``too-many-ancestors``.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods
from collections.abc import Callable, Container, Hashable, Iterable, Sized


class FromIgnoredAbcs(Iterable, Sized, Container, Hashable):
    def __iter__(self):
        return iter(())

    def __len__(self):
        return 0

    def __contains__(self, item):
        return False

    def __hash__(self):
        return 0


class FromCallable(Callable):
    def __call__(self):
        pass


class FromCallableAndOthers(Callable, Iterable, Sized):
    def __call__(self):
        pass

    def __iter__(self):
        return iter(())

    def __len__(self):
        return 0

"""Check non-iterators returned by __iter__ """

# pylint: disable=too-few-public-methods, missing-docstring, consider-using-with, import-error, use-yield-from
from uninferable import UNINFERABLE

class FirstGoodIterator:
    """ yields in iterator. """

    def __iter__(self):
        for index in range(10):
            yield index


class SecondGoodIterator:
    """ __iter__ and next """

    def __iter__(self):
        return self

    def __next__(self):
        """ Infinite iterator, but still an iterator """
        return 1

    def next(self):
        """Same as __next__, but for Python 2."""
        return 1


class ThirdGoodIterator:
    """ Returns other iterator, not the current instance """

    def __iter__(self):
        return SecondGoodIterator()


class FourthGoodIterator:
    """ __iter__ returns iter(...) """

    def __iter__(self):
        return iter(range(10))


class IteratorMetaclass(type):
    def __next__(cls):
        return 1

    def next(cls):
        return 2


class IteratorClass(metaclass=IteratorMetaclass):
    """Iterable through the metaclass."""


class FifthGoodIterator:
    """__iter__ returns a class which uses an iterator-metaclass."""

    def __iter__(self):
        return IteratorClass


class FileBasedIterator:
    def __init__(self, path):
        self.path = path
        self.file = None

    def __iter__(self):
        if self.file is not None:
            self.file.close()
        self.file = open(self.path, encoding="utf-8")
        # self file has two inferred values: None and <instance of 'file'>
        # we don't want to emit error in this case
        return self.file


class FirstBadIterator:
    """ __iter__ returns a list """

    def __iter__(self):  # [non-iterator-returned]
        return []


class SecondBadIterator:
    """ __iter__ without next """

    def __iter__(self):  # [non-iterator-returned]
        return self


class ThirdBadIterator:
    """ __iter__ returns an instance of another non-iterator """

    def __iter__(self):  # [non-iterator-returned]
        return SecondBadIterator()


class FourthBadIterator:
    """__iter__ returns a class."""

    def __iter__(self):  # [non-iterator-returned]
        return ThirdBadIterator

class SixthGoodIterator:
    """__iter__ returns Uninferable."""

    def __iter__(self):
        return UNINFERABLE

"""Check that instantiating a class with
`abc.ABCMeta` as metaclass fails if it defines
abstract methods.
"""

# pylint: disable=too-few-public-methods, missing-docstring
# pylint: disable=abstract-method, import-error

import abc
import weakref
from lala import Bala
import pandas as pd


class GoodClass(metaclass=abc.ABCMeta):
    pass

class SecondGoodClass(metaclass=abc.ABCMeta):
    def test(self):
        """ do nothing. """

class ThirdGoodClass(metaclass=abc.ABCMeta):
    """ This should not raise the warning. """
    def test(self):
        raise NotImplementedError()

class BadClass(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def test(self):
        """ do nothing. """

class SecondBadClass(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def test(self):
        """ do nothing. """

class ThirdBadClass(SecondBadClass):
    pass


class Structure(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __iter__(self):
        pass
    @abc.abstractmethod
    def __len__(self):
        pass
    @abc.abstractmethod
    def __contains__(self, _):
        pass
    @abc.abstractmethod
    def __hash__(self):
        pass

class Container(Structure):
    def __contains__(self, _):
        pass

class Sizable(Structure):
    def __len__(self):
        return 42

class Hashable(Structure):
    __hash__ = 42


class Iterator(Structure):
    def keys(self):
        return iter([1, 2, 3])

    __iter__ = keys

class AbstractSizable(Structure):
    @abc.abstractmethod
    def length(self):
        pass
    __len__ = length

class NoMroAbstractMethods(Container, Iterator, Sizable, Hashable):
    pass

class BadMroAbstractMethods(Container, Iterator, AbstractSizable):
    pass

class SomeMetaclass(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prop(self):
        pass

class FourthGoodClass(SomeMetaclass):
    """Don't consider this abstract if some attributes are
    there, but can't be inferred.
    """
    prop = Bala # missing


def main():
    """ do nothing """
    GoodClass()
    SecondGoodClass()
    ThirdGoodClass()
    FourthGoodClass()
    weakref.WeakKeyDictionary()
    weakref.WeakValueDictionary()
    NoMroAbstractMethods()

    BadMroAbstractMethods() # [abstract-class-instantiated]
    BadClass() # [abstract-class-instantiated]
    SecondBadClass() # [abstract-class-instantiated]
    ThirdBadClass() # [abstract-class-instantiated]


if 1: # pylint: disable=using-constant-test
    class FourthBadClass(metaclass=abc.ABCMeta):

        def test(self):
            pass
else:
    class FourthBadClass(metaclass=abc.ABCMeta):

        @abc.abstractmethod
        def test(self):
            pass


def main2():
    FourthBadClass() # [abstract-class-instantiated]


class BadClassTwo(abc.ABC):
    """
    Check that instantiating a class with `abc.ABCMeta` as ancestor fails if it
    defines abstract methods.
    """
    @abc.abstractmethod
    def test(self):
        pass


def main_two():
    """ do nothing """
    BadClassTwo() # [abstract-class-instantiated]


# Testcase from https://github.com/PyCQA/pylint/issues/3060
with pd.ExcelWriter("demo.xlsx") as writer:
    print(writer)

class GoodWithNew(metaclass=abc.ABCMeta):
    def __new__(cls):
        pass

    @property
    @abc.abstractmethod
    def sheets(self):
        """sheets."""

    @property
    @abc.abstractmethod
    def book(self):
        """book."""

test = GoodWithNew()


class BadWithNew(metaclass=abc.ABCMeta):
    def __new__(cls):
        print("Test.__new__")
        return super().__new__(cls)

    @property
    @abc.abstractmethod
    def sheets(self):
        """sheets."""

    @property
    @abc.abstractmethod
    def book(self):
        """book."""

test = BadWithNew()  # [abstract-class-instantiated]

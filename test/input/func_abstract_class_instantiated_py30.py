"""Check that instantiating a class with
`abc.ABCMeta` as metaclass fails if it defines
abstract methods.
"""

# pylint: disable=too-few-public-methods, missing-docstring, abstract-class-not-used

__revision__ = 0

import abc

class GoodClass(object, metaclass=abc.ABCMeta):
    pass

class SecondGoodClass(object, metaclass=abc.ABCMeta):
    def test(self):
        """ do nothing. """
        pass

class ThirdGoodClass(object, metaclass=abc.ABCMeta):
    """ This should not raise the warning. """
    def test(self):
        raise NotImplementedError()

class BadClass(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def test(self):
        """ do nothing. """
        pass

class SecondBadClass(object, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def test(self):
        """ do nothing. """

def main():
    """ do nothing """
    GoodClass()
    SecondGoodClass()
    ThirdGoodClass()
    BadClass()
    SecondBadClass()

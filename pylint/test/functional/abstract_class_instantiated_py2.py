"""Check that instantiating a class with
`abc.ABCMeta` as metaclass fails if it defines
abstract methods.
"""

# pylint: disable=too-few-public-methods, missing-docstring
# pylint: disable=no-absolute-import, metaclass-assignment
# pylint: disable=abstract-method

__revision__ = 0

import abc
from abc import ABCMeta

class GoodClass(object):
    __metaclass__ = abc.ABCMeta

class SecondGoodClass(object):
    __metaclass__ = abc.ABCMeta

    def test(self):
        """ do nothing. """

class ThirdGoodClass(object):
    __metaclass__ = abc.ABCMeta

    def test(self):
        raise NotImplementedError()

class FourthGoodClass(object):
    __metaclass__ = ABCMeta

class BadClass(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def test(self):
        """ do nothing. """

class SecondBadClass(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def test(self):
        """ do nothing. """

class ThirdBadClass(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def test(self):
        pass

class FourthBadClass(ThirdBadClass):
    pass


def main():
    """ do nothing """
    GoodClass()
    SecondGoodClass()
    ThirdGoodClass()
    FourthGoodClass()
    BadClass() # [abstract-class-instantiated]
    SecondBadClass() # [abstract-class-instantiated]
    ThirdBadClass() # [abstract-class-instantiated]
    FourthBadClass() # [abstract-class-instantiated]

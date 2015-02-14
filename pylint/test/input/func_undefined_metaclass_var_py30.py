"""test access to undefined variables in Python 3 metaclass syntax """
# pylint: disable=no-init, invalid-name, too-few-public-methods
__revision__ = '$Id:'

import abc
from abc import ABCMeta

class Bad(metaclass=ABCMet):
    """ Notice the typo """

class SecondBad(metaclass=ab.ABCMeta):
    """ Notice the `ab` module. """

class Good(metaclass=int):
    """ int is not a proper metaclass, but it is defined. """

class SecondGood(metaclass=Good):
    """ empty """

class ThirdGood(metaclass=ABCMeta):
    """ empty """

class FourthGood(ThirdGood):
    """ This should not trigger anything. """

data = abc
testdata = ABCMeta

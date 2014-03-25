""" This should not warn about `prop` being abstract in Child """

# pylint: disable=too-few-public-methods,abstract-class-little-used,no-init,old-style-class

__revision__ = None

import abc

class Parent(metaclass=abc.ABCMeta):
    """ Class """

    @property
    @abc.abstractmethod
    def prop(self):
        """ Abstract """

class Child(Parent):
    """ No warning for the following. """
    prop = property(lambda self: 1)

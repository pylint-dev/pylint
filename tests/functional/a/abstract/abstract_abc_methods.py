""" This should not warn about `prop` being abstract in Child """
# pylint: disable=too-few-public-methods

import abc

class Parent:
    """Abstract Base Class """
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def prop(self):
        """ Abstract """

class Child(Parent):
    """ No warning for the following. """
    prop = property(lambda self: 1)

"""Don't warn if the class is instantiated in its own body."""
# pylint: disable=missing-docstring, useless-object-inheritance


import abc


class Ala(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def bala(self):
        pass

    @classmethod
    def portocala(cls):
        instance = cls()
        return instance

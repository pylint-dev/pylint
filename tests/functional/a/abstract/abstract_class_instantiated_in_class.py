"""Don't warn if the class is instantiated in its own body."""
# pylint: disable=missing-docstring


import abc


class Ala(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def bala(self):
        pass

    @classmethod
    def portocala(cls):
        instance = cls()
        return instance

# pylint: disable=missing-docstring, too-few-public-methods, import-error,unused-argument

import abc

import six
from unknown import Unknown


class InvalidAsMetaclass:
    pass


class ValidAsMetaclass(type):
    pass


@six.add_metaclass(type)
class FirstGood:
    pass


@six.add_metaclass(abc.ABCMeta)
class SecondGood:
    pass


@six.add_metaclass(Unknown)
class ThirdGood:
    pass


@six.add_metaclass(ValidAsMetaclass)
class FourthGood:
    pass


class FirstInvalid(metaclass=int):  # [invalid-metaclass]
    pass


class SecondInvalid(metaclass=InvalidAsMetaclass):  # [invalid-metaclass]
    pass


class ThirdInvalid(metaclass=2):  # [invalid-metaclass]
    pass


class FourthInvalid(metaclass=InvalidAsMetaclass()):  # [invalid-metaclass]
    pass


def invalid_metaclass_1(name, bases, attrs):
    return int


def invalid_metaclass_2(name, bases, attrs):
    return 1


class Invalid(metaclass=invalid_metaclass_1):  # [invalid-metaclass]
    pass


class InvalidSecond(metaclass=invalid_metaclass_2):  # [invalid-metaclass]
    pass

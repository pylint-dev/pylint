# pylint: disable=missing-docstring, too-few-public-methods, import-error,unused-argument, useless-object-inheritance

import abc

import six
from unknown import Unknown


class InvalidAsMetaclass(object):
    pass


class ValidAsMetaclass(type):
    pass


@six.add_metaclass(type)
class FirstGood(object):
    pass


@six.add_metaclass(abc.ABCMeta)
class SecondGood(object):
    pass


@six.add_metaclass(Unknown)
class ThirdGood(object):
    pass


@six.add_metaclass(ValidAsMetaclass)
class FourthGood(object):
    pass


class FirstInvalid(object, metaclass=int):  # [invalid-metaclass]
    pass


class SecondInvalid(object, metaclass=InvalidAsMetaclass):  # [invalid-metaclass]
    pass


class ThirdInvalid(object, metaclass=2):  # [invalid-metaclass]
    pass


class FourthInvalid(object, metaclass=InvalidAsMetaclass()):  # [invalid-metaclass]
    pass


def invalid_metaclass_1(name, bases, attrs):
    return int


def invalid_metaclass_2(name, bases, attrs):
    return 1


class Invalid(metaclass=invalid_metaclass_1):  # [invalid-metaclass]
    pass


class InvalidSecond(metaclass=invalid_metaclass_2):  # [invalid-metaclass]
    pass

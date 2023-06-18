# pylint: disable=missing-docstring, too-few-public-methods, import-error,unused-argument

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

import abc
from pathlib import Path
from typing import Protocol

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


class MetaclassWithInvalidMRO(type(object), type(object)):  # [duplicate-bases]
    pass


class FifthInvalid(metaclass=MetaclassWithInvalidMRO):  # [invalid-metaclass]
    pass


class Proto(Protocol):
    ...


class MetaclassWithInconsistentMRO(type(Path), type(Proto)):  # [inconsistent-mro]
    pass


class SixthInvalid(  # [invalid-metaclass]
    Path, Proto, metaclass=MetaclassWithInconsistentMRO
):
    pass

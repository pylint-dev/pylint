# pylint: disable=missing-docstring,invalid-name,too-few-public-methods

# https://github.com/PyCQA/pylint/issues/2822
# Base should be subscriptable, even with ABCMeta as metaclass
from abc import ABCMeta
from typing import Generic, TypeVar

T = TypeVar("T")

class Base(Generic[T], metaclass=ABCMeta):
    """Base"""

class Impl(Base[str]):
    """Impl"""

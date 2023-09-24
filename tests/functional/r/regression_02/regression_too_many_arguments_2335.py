"""Test that `abc.ABCMeta.__new__` does not trigger too-many-function-arguments when referred

https://github.com/pylint-dev/pylint/issues/2335
"""
# pylint: disable=missing-class-docstring,unused-argument,arguments-differ
from abc import ABCMeta


class NodeCheckMetaClass(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        return ABCMeta.__new__(mcs, name, bases, namespace)

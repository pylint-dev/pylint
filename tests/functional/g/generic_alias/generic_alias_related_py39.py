"""Test related function for generic alias.

Any solution should not change the behavior of
- `__getitem__`
- `__class_getitem__`
- `metaclass=ABCMeta`
"""
# flake8: noqa
# pylint: disable=missing-docstring,pointless-statement,expression-not-assigned
# pylint: disable=too-few-public-methods,multiple-statements,line-too-long
from abc import ABCMeta, abstractmethod
import typing

GenericAlias = type(list[int])


class ClsUnsubscriptable:
    def __init__(self):
        pass

class ClsGetItem:
    def __init__(self):
        self.var = [1, 2, 3, 4]
    def __getitem__(self, item):
        return self.var[item]

class ClsClassGetItem:
    def __init__(self):
        pass
    __class_getitem__ = classmethod(GenericAlias)

class ClsList(typing.List):
    pass


ClsUnsubscriptable()[1]  # [unsubscriptable-object]
ClsUnsubscriptable[int]  # [unsubscriptable-object]

ClsGetItem()[1]
ClsGetItem[int]  # [unsubscriptable-object]

ClsClassGetItem()[1]  # [unsubscriptable-object]
ClsClassGetItem[int]

# subscriptable because of inheritance
ClsList([0, 1, 2])[1]
ClsList[int]


class ClsAbstract(metaclass=ABCMeta):
    @abstractmethod
    def abstract_method(self):
        pass

class Derived(ClsAbstract):  # [abstract-method]
    pass

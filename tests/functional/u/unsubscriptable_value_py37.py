# pylint: disable=missing-class-docstring,too-few-public-methods,pointless-statement,expression-not-assigned
"""
Checks that class used in a subscript supports subscription
(i.e. defines __class_getitem__ method).
"""
import typing


class Subscriptable:

    def __class_getitem__(cls, params):
        pass

Subscriptable[0]
Subscriptable()[0]  # [unsubscriptable-object]

a: typing.List[int]

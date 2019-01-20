"""
Checks that class used in a subscript supports subscription
(i.e. defines __class_getitem__ method).
"""
# pylint: disable=missing-docstring,pointless-statement,expression-not-assigned,wrong-import-position
# pylint: disable=too-few-public-methods,import-error,invalid-name,wrong-import-order, useless-object-inheritance

import typing

class Subscriptable(object):

    def __class_getitem__(cls, params):
        pass


Subscriptable[0]
Subscriptable()[0]  # [unsubscriptable-object]

a: typing.List[int]

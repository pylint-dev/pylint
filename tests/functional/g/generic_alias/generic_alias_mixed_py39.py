"""Test generic alias support with mix of typing.py and stdlib types (PY39+)."""
# flake8: noqa
# pylint: disable=missing-docstring,pointless-statement
# pylint: disable=too-few-public-methods,multiple-statements,line-too-long
import collections
import collections.abc
import contextlib
import re
import typing

# Type annotations
var_orderedDict: collections.OrderedDict[int, str]
var_container: collections.abc.Container[int]
var_sequence: collections.abc.Sequence[int]
var_iterable: collections.abc.Iterable[int]
var_awaitable: collections.abc.Awaitable[int]
var_pattern: re.Pattern[int]
var_bytestring: collections.abc.ByteString
var_hashable: collections.abc.Hashable
var_ContextManager: contextlib.AbstractContextManager[int]


# No implementation required for 'builtins'
class DerivedListIterable(typing.List[typing.Iterable[int]]):
    pass


# Missing implementation for 'collections.abc' derived classes
class DerivedHashable(typing.Hashable):  # [abstract-method]  # __hash__
    pass

class DerivedIterable(typing.Iterable[int]):  # [abstract-method]  # __iter__
    pass

class DerivedCollection(typing.Collection[int]):  # [abstract-method,abstract-method,abstract-method]  # __contains__, __iter__, __len__
    pass

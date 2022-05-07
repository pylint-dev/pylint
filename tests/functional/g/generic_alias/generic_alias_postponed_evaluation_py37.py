"""Test generic alias support for stdlib types (added in PY39).

In type annotation context, they can be used with postponed evaluation enabled,
starting with PY37.
"""
# flake8: noqa
# pylint: disable=missing-docstring,pointless-statement,invalid-name
# pylint: disable=too-few-public-methods,multiple-statements,line-too-long
from __future__ import annotations

import abc
import collections
import collections.abc
import contextlib
import re


# ----- unsubscriptable (even with postponed evaluation) -----
# special
tuple[int, int]  # [unsubscriptable-object]
type[int]  # [unsubscriptable-object]
collections.abc.Callable[[int], str]  # [unsubscriptable-object]

# builtins
dict[int, str]  # [unsubscriptable-object]
list[int]  # [unsubscriptable-object]
set[int]  # [unsubscriptable-object]
frozenset[int]  # [unsubscriptable-object]

# collections
collections.defaultdict[int, str]  # [unsubscriptable-object]
collections.OrderedDict[int, str]  # [unsubscriptable-object]
collections.ChainMap[int, str]  # [unsubscriptable-object]
collections.Counter[int]  # [unsubscriptable-object]
collections.deque[int]  # [unsubscriptable-object]

# collections.abc
collections.abc.Set[int]  # [unsubscriptable-object]
collections.abc.Collection[int]  # [unsubscriptable-object]
collections.abc.Container[int]  # [unsubscriptable-object]
collections.abc.ItemsView[int, str]  # [unsubscriptable-object]
collections.abc.KeysView[int]  # [unsubscriptable-object]
collections.abc.Mapping[int, str]  # [unsubscriptable-object]
collections.abc.MappingView[int]  # [unsubscriptable-object]
collections.abc.MutableMapping[int, str]  # [unsubscriptable-object]
collections.abc.MutableSequence[int]  # [unsubscriptable-object]
collections.abc.MutableSet[int]  # [unsubscriptable-object]
collections.abc.Sequence[int]  # [unsubscriptable-object]
collections.abc.ValuesView[int]  # [unsubscriptable-object]

collections.abc.Iterable[int]  # [unsubscriptable-object]
collections.abc.Iterator[int]  # [unsubscriptable-object]
collections.abc.Generator[int, None, None]  # [unsubscriptable-object]
collections.abc.Reversible[int]  # [unsubscriptable-object]

collections.abc.Coroutine[list[str], str, int]  # [unsubscriptable-object,unsubscriptable-object]
collections.abc.AsyncGenerator[int, None]  # [unsubscriptable-object]
collections.abc.AsyncIterable[int]  # [unsubscriptable-object]
collections.abc.AsyncIterator[int]  # [unsubscriptable-object]
collections.abc.Awaitable[int]  # [unsubscriptable-object]

# contextlib
contextlib.AbstractContextManager[int]  # [unsubscriptable-object]
contextlib.AbstractAsyncContextManager[int]  # [unsubscriptable-object]

# re
re.Pattern[str]  # [unsubscriptable-object]
re.Match[str]  # [unsubscriptable-object]


# unsubscriptable types
collections.abc.Hashable
collections.abc.Sized
collections.abc.Hashable[int]  # [unsubscriptable-object]
collections.abc.Sized[int]  # [unsubscriptable-object]

# subscriptable with Python 3.9
collections.abc.ByteString[int]  # [unsubscriptable-object]


# Missing implementation for 'collections.abc' derived classes
class DerivedHashable(collections.abc.Hashable):  # [abstract-method]  # __hash__
    pass

class DerivedIterable(collections.abc.Iterable[int]):  # [unsubscriptable-object]
    pass

class DerivedCollection(collections.abc.Collection[int]):  # [unsubscriptable-object]
    pass


# No implementation required for 'builtins' and 'collections' types
class DerivedList(list[int]):  # [unsubscriptable-object]
    pass

class DerivedSet(set[int]):  # [unsubscriptable-object]
    pass

class DerivedOrderedDict(collections.OrderedDict[int, str]):  # [unsubscriptable-object]
    pass

class DerivedListIterable(list[collections.abc.Iterable[int]]):  # [unsubscriptable-object,unsubscriptable-object]
    pass


# Multiple generic base classes
class DerivedMultiple(collections.abc.Sized, collections.abc.Hashable):  # [abstract-method,abstract-method]
    pass

class CustomAbstractCls1(abc.ABC):
    pass
class CustomAbstractCls2(collections.abc.Sized, collections.abc.Iterable[CustomAbstractCls1]):  # [abstract-method,unsubscriptable-object]  # __len__
    pass
class CustomImplementation(CustomAbstractCls2):  # [abstract-method]  # __len__
    pass



# ----- subscriptable (with postponed evaluation) -----
# special
var_tuple: tuple[int, int]
var_type: type[int]
var_callable: collections.abc.Callable[[int], str]

# builtins
var_dict: dict[int, str]
var_list: list[int]
var_set: set[int]
var_frozenset: frozenset[int]

# collections
var_defaultdict: collections.defaultdict[int, str]
var_OrderedDict: collections.OrderedDict[int, str]
var_ChainMap: collections.ChainMap[int, str]
var_Counter: collections.Counter[int]
var_deque: collections.deque[int]

# collections.abc
var_abc_set: collections.abc.Set[int]
var_abc_collection: collections.abc.Collection[int]
var_abc_container: collections.abc.Container[int]
var_abc_ItemsView: collections.abc.ItemsView[int, str]
var_abc_KeysView: collections.abc.KeysView[int]
var_abc_Mapping: collections.abc.Mapping[int, str]
var_abc_MappingView: collections.abc.MappingView[int]
var_abc_MutableMapping: collections.abc.MutableMapping[int, str]
var_abc_MutableSequence: collections.abc.MutableSequence[int]
var_abc_MutableSet: collections.abc.MutableSet[int]
var_abc_Sequence: collections.abc.Sequence[int]
var_abc_ValuesView: collections.abc.ValuesView[int]

var_abc_Iterable: collections.abc.Iterable[int]
var_abc_Iterator: collections.abc.Iterator[int]
var_abc_Generator: collections.abc.Generator[int, None, None]
var_abc_Reversible: collections.abc.Reversible[int]

var_abc_Coroutine: collections.abc.Coroutine[list[str], str, int]
var_abc_AsyncGenerator: collections.abc.AsyncGenerator[int, None]
var_abc_AsyncIterable: collections.abc.AsyncIterable[int]
var_abc_AsyncIterator: collections.abc.AsyncIterator[int]
var_abc_Awaitable: collections.abc.Awaitable[int]

# contextlib
var_ContextManager: contextlib.AbstractContextManager[int]
var_AsyncContextManager: contextlib.AbstractAsyncContextManager[int]

# re
var_re_Pattern: re.Pattern[str]
var_re_Match: re.Match[str]


# unsubscriptable types
var_abc_Hashable: collections.abc.Hashable
var_abc_Sized: collections.abc.Sized
var_abc_Hashable2: collections.abc.Hashable[int]  # string annotations aren't checked
var_abc_Sized2: collections.abc.Sized[int]  # string annotations aren't checked

# subscriptable with Python 3.9
var_abc_ByteString: collections.abc.ByteString[int]


# Generic in type stubs only -> string annotations aren't checked
class A:
    ...

var_a1: A[str]  # string annotations aren't checked
var_a2: "A[str]"  # string annotations aren't checked
class B(A[str]):  # [unsubscriptable-object]
    ...

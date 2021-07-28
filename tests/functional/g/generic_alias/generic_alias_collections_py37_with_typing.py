"""Test generic alias support for stdlib types (added in PY39).

Raise [unsubscriptable-object] error for PY37 and PY38.
Make sure `import typing` doesn't change anything.
"""
# flake8: noqa
# pylint: disable=missing-docstring,pointless-statement,unused-import
# pylint: disable=too-few-public-methods,multiple-statements,line-too-long
import abc
import collections
import collections.abc
import contextlib
import re
import typing

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


# Type annotations
var_tuple: tuple[int, int]  # [unsubscriptable-object]
var_dict: dict[int, str]  # [unsubscriptable-object]
var_orderedDict: collections.OrderedDict[int, str]  # [unsubscriptable-object]
var_container: collections.abc.Container[int]  # [unsubscriptable-object]
var_sequence: collections.abc.Sequence[int]  # [unsubscriptable-object]
var_iterable: collections.abc.Iterable[int]  # [unsubscriptable-object]
var_awaitable: collections.abc.Awaitable[int]  # [unsubscriptable-object]
var_contextmanager: contextlib.AbstractContextManager[int]  # [unsubscriptable-object]
var_pattern: re.Pattern[int]  # [unsubscriptable-object]
var_bytestring: collections.abc.ByteString
var_hashable: collections.abc.Hashable
var_sized: collections.abc.Sized

# Type annotation with unsubscriptable type
var_int: int[int]  # [unsubscriptable-object]
var_hashable2: collections.abc.Hashable[int]  # [unsubscriptable-object]
var_sized2: collections.abc.Sized[int]  # [unsubscriptable-object]

# subscriptable with Python 3.9
var_bytestring2: collections.abc.ByteString[int]  # [unsubscriptable-object]

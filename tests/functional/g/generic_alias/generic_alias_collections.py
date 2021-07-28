"""Test generic alias support for stdlib types (added in PY39)."""
# flake8: noqa
# pylint: disable=missing-docstring,pointless-statement
# pylint: disable=too-few-public-methods,multiple-statements,line-too-long
import abc
import collections
import collections.abc
import contextlib
import re

# special
tuple[int, int]
type[int]
collections.abc.Callable[[int], str]

# builtins
dict[int, str]
list[int]
set[int]
frozenset[int]

# collections
collections.defaultdict[int, str]
collections.OrderedDict[int, str]
collections.ChainMap[int, str]
collections.Counter[int]
collections.deque[int]

# collections.abc
collections.abc.Set[int]
collections.abc.Collection[int]
collections.abc.Container[int]
collections.abc.ItemsView[int, str]
collections.abc.KeysView[int]
collections.abc.Mapping[int, str]
collections.abc.MappingView[int]
collections.abc.MutableMapping[int, str]
collections.abc.MutableSequence[int]
collections.abc.MutableSet[int]
collections.abc.Sequence[int]
collections.abc.ValuesView[int]

collections.abc.Iterable[int]
collections.abc.Iterator[int]
collections.abc.Generator[int, None, None]
collections.abc.Reversible[int]

collections.abc.Coroutine[list[str], str, int]
collections.abc.AsyncGenerator[int, None]
collections.abc.AsyncIterable[int]
collections.abc.AsyncIterator[int]
collections.abc.Awaitable[int]

# contextlib
contextlib.AbstractContextManager[int]
contextlib.AbstractAsyncContextManager[int]

# re
re.Pattern[str]
re.Match[str]


# unsubscriptable types
collections.abc.Hashable
collections.abc.Sized
collections.abc.Hashable[int]  # [unsubscriptable-object]
collections.abc.Sized[int]  # [unsubscriptable-object]

# subscriptable with Python 3.9
collections.abc.ByteString[int]


# Missing implementation for 'collections.abc' derived classes
class DerivedHashable(collections.abc.Hashable):  # [abstract-method]  # __hash__
    pass

class DerivedIterable(collections.abc.Iterable[int]):  # [abstract-method]  # __iter__
    pass

class DerivedCollection(collections.abc.Collection[int]):  # [abstract-method,abstract-method,abstract-method]  # __contains__, __iter__, __len__
    pass


# No implementation required for 'builtins' and 'collections' types
class DerivedList(list[int]):
    pass

class DerivedSet(set[int]):
    pass

class DerivedOrderedDict(collections.OrderedDict[int, str]):
    pass

class DerivedListIterable(list[collections.abc.Iterable[int]]):
    pass


# Multiple generic base classes
class DerivedMultiple(collections.abc.Sized, collections.abc.Hashable):  # [abstract-method,abstract-method]
    pass

class CustomAbstractCls1(abc.ABC):
    pass
class CustomAbstractCls2(collections.abc.Sized, collections.abc.Iterable[CustomAbstractCls1]):  # [abstract-method,abstract-method]  # __iter__, __len__
    pass
class CustomImplementation(CustomAbstractCls2):  # [abstract-method,abstract-method]  # __iter__, __len__
    pass


# Type annotations
var_tuple: tuple[int, int]
var_dict: dict[int, str]
var_orderedDict: collections.OrderedDict[int, str]
var_container: collections.abc.Container[int]
var_sequence: collections.abc.Sequence[int]
var_iterable: collections.abc.Iterable[int]
var_awaitable: collections.abc.Awaitable[int]
var_contextmanager: contextlib.AbstractContextManager[int]
var_pattern: re.Pattern[int]
var_bytestring: collections.abc.ByteString
var_hashable: collections.abc.Hashable
var_sized: collections.abc.Sized

# Type annotation with unsubscriptable type
var_int: int[int]  # [unsubscriptable-object]
var_hashable2: collections.abc.Hashable[int]  # [unsubscriptable-object]
var_sized2: collections.abc.Sized[int]  # [unsubscriptable-object]

# subscriptable with Python 3.9
var_bytestring2: collections.abc.ByteString[int]

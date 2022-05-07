"""Test generic alias support for typing.py types."""
# flake8: noqa
# pylint: disable=missing-docstring,pointless-statement,invalid-name
# pylint: disable=too-few-public-methods,multiple-statements,line-too-long, unnecessary-dunder-call
import abc
import typing

# special
typing.Tuple[int, int]
typing.Type[int]
typing.Callable[[int], str]

# builtins
typing.Dict[int, str]
typing.List[int]
typing.Set[int]
typing.FrozenSet[int]

# collections
typing.DefaultDict[int, str]
typing.OrderedDict[int, str]
typing.ChainMap[int, str]
typing.Counter[int]
typing.Deque[int]

# collections.abc
typing.AbstractSet[int]
typing.Collection[int]
typing.Container[int]
typing.ItemsView[int, str]
typing.KeysView[int]
typing.Mapping[int, str]
typing.MappingView[int]
typing.MutableMapping[int, str]
typing.MutableSequence[int]
typing.MutableSet[int]
typing.Sequence[int]
typing.ValuesView[int]

typing.Iterable[int]
typing.Iterator[int]
typing.Generator[int, None, None]
typing.Reversible[int]

typing.Coroutine[typing.List[str], str, int]
typing.AsyncGenerator[int, None]
typing.AsyncIterable[int]
typing.AsyncIterator[int]
typing.Awaitable[int]

# contextlib
typing.ContextManager[int]
typing.AsyncContextManager[int]

# re
typing.Pattern[str]
typing.Match[str]
typing.re.Pattern[str]
typing.re.Match[str]


# unsubscriptable types
typing.ByteString
typing.Hashable
typing.Sized
typing.ByteString[int]  # [unsubscriptable-object]
typing.Hashable[int]  # [unsubscriptable-object]
typing.Sized[int]  # [unsubscriptable-object]


# Missing implementation for 'collections.abc' derived classes
class DerivedHashable(typing.Hashable):  # [abstract-method]  # __hash__
    pass

class DerivedIterable(typing.Iterable[int]):  # [abstract-method]  # __iter__
    pass

class DerivedCollection(typing.Collection[int]):  # [abstract-method,abstract-method,abstract-method]  # __contains__, __iter__, __len__
    pass


# No implementation required for 'builtins' and 'collections' types
class DerivedList(typing.List[int]):
    def func(self):
        return self.__iter__()

class DerivedSet(typing.Set[int]):
    def func(self):
        return self.add(2)

class DerivedOrderedDict(typing.OrderedDict[int, str]):
    def func(self):
        return self.items()

class DerivedListIterable(typing.List[typing.Iterable[int]]):
    pass


# Multiple generic base classes
class DerivedMultiple(typing.Sized, typing.Hashable):  # [abstract-method,abstract-method]
    pass

class CustomAbstractCls1(abc.ABC):
    pass
class CustomAbstractCls2(typing.Sized, typing.Iterable[CustomAbstractCls1]):  # [abstract-method,abstract-method]  # __iter__, __len__
    pass
class CustomImplementation(CustomAbstractCls2):  # [abstract-method,abstract-method]  # __iter__, __len__
    pass


# Inheritance without generic
class DerivedList2(typing.List):
    pass

class DerivedOrderedDict2(typing.OrderedDict):
    pass

class DerivedIterable2(typing.Iterable):  # [abstract-method]  # __iter__
    pass


# Type annotations
var_tuple: typing.Tuple[int, int]
var_dict: typing.Dict[int, str]
var_orderedDict: typing.OrderedDict[int, str]
var_container: typing.Container[int]
var_sequence: typing.Sequence[int]
var_iterable: typing.Iterable[int]
var_awaitable: typing.Awaitable[int]
var_contextmanager: typing.ContextManager[int]
var_pattern: typing.Pattern[int]
var_pattern2: typing.re.Pattern[int]
var_bytestring: typing.ByteString
var_hashable: typing.Hashable
var_sized: typing.Sized

# Type annotation with unsubscriptable type
var_int: int[int]  # [unsubscriptable-object]
var_bytestring2: typing.ByteString[int]  # [unsubscriptable-object]
var_hashable2: typing.Hashable[int]  # [unsubscriptable-object]
var_sized2: typing.Sized[int]  # [unsubscriptable-object]


# Generic in type stubs only -> string annotations aren't checked
class A:
    ...

var_a1: A[str]  # [unsubscriptable-object]
var_a2: "A[str]"  # string annotations aren't checked
class B(A[str]):  # [unsubscriptable-object]
    ...

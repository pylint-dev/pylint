# pylint: disable=invalid-name,missing-docstring,pointless-statement,expression-not-assigned,unnecessary-comprehension,undefined-variable,bad-chained-comparison,too-few-public-methods,unused-argument

import dataclasses

x = 1
var = frozenset({1, 2, 3})

x in var
x in {1, 2, 3}
x in (1, 2, 3)  # [use-set-for-membership]
x in [1, 2, 3]  # [use-set-for-membership]

if x in var:
    pass
if x in {1, 2, 3}:
    pass
if x in (1, 2, 3):  # [use-set-for-membership]
    pass
if x in [1, 2, 3]:  # [use-set-for-membership]
    pass

42 if x in [1, 2, 3] else None  # [use-set-for-membership]
assert x in [1, 2, 3]  # [use-set-for-membership]
(x for x in var if x in [1, 2, 3])  # [use-set-for-membership]
while x in [1, 2, 3]:  # [use-set-for-membership]
    break

# Stacked operators, rightmost pair is evaluated first
# Doesn't make much sense in practice since `in` will only return `bool`
True == x in [1, 2, 3]  # [use-set-for-membership]  # noqa: E712
1 >= x in [1, 2, 3]  # [use-set-for-membership]  # noqa: E712


# Test hashable heuristic
x in (1, "Hello World", False, None)  # [use-set-for-membership]
x in (1, [])  # List is not hashable

if x:
    var2 = 2
else:
    var2 = []
x in (1, var2)  # var2 can be a list


# Hashable and unhashable classes and instances (issue #4933)
class Hashable:
    pass


class NotHashable:
    def __eq__(self, other):
        return True


class HashableAgain:
    def __eq__(self, other):
        return True

    def __hash__(self):
        return 1


class SubHashable(Hashable):
    pass


class SubNotHashable(NotHashable):
    pass


class SubHashableAgain(NotHashable):
    def __hash__(self):
        return 1


class ExplicitNoneHash:
    __hash__ = None


class ListHash:
    __hash__ = list.__hash__


class ObjectHash:
    __hash__ = object.__hash__


class HashableMeta(type):
    pass


class UnhashableMeta(type):
    __hash__ = None


class ClassWithHashableMeta(metaclass=HashableMeta):
    pass


class ClassWithUnhashableMeta(metaclass=UnhashableMeta):
    pass


def make_class(name, bases, namespace):
    return type(name, bases, namespace)


class ClassWithFuncMeta(metaclass=make_class):
    pass


@dataclasses.dataclass
class NonFrozenDC:
    a: int


@dataclasses.dataclass
class HashableDC:
    a: int

    def __hash__(self):
        return 1


def my_func():
    pass


# Class objects (hashable when metaclass is hashable)
x in (Hashable, HashableAgain, NotHashable)  # [use-set-for-membership]
x in [1, ClassWithHashableMeta]  # [use-set-for-membership]
x in [1, ClassWithUnhashableMeta]
x in [1, ClassWithFuncMeta]

# Instances
x in [Hashable(), HashableAgain(), SubHashable()]  # [use-set-for-membership]
x in [SubHashableAgain(), ObjectHash(), HashableDC(1)]  # [use-set-for-membership]
x in [NotHashable()]
x in [SubNotHashable()]
x in [ExplicitNoneHash()]
x in [ListHash()]
x in [NonFrozenDC(1)]

# Functions, lambdas, modules, methods, and variables inferred to hashable values
h_obj = Hashable()
x in (1, my_func, lambda y: y, dataclasses, h_obj, h_obj.__repr__)  # [use-set-for-membership]

# Nested tuples, starred elements, and mutable containers
hashable_tuple = (1, Hashable())
x in (1, (2, Hashable()))  # [use-set-for-membership]
x in [1, hashable_tuple]  # [use-set-for-membership]
x in (1, (2, []))
x in [1, *var]
x in [1, {1: 2}]
x in [1, {1}]
x in [1, [i for i in var]]


# Uninferable, InferenceError, MroError, dynamic tuple, and cyclic tuple
def check_edge_cases(param):
    class UnknownHash:
        __hash__ = unknown_hash

    class ClassWithUninferableMeta(metaclass=UnknownMeta):
        pass

    class BadMRO(Hashable, SubHashable):  # pylint: disable=inconsistent-mro
        pass

    class DynamicBase(UnknownBase):
        pass

    def get_cyclic():
        return cyclic_tuple

    cyclic_tuple = (get_cyclic(),)

    _ = x in (1, param)
    _ = x in (1, tuple(param))
    _ = x in (1, undefined_name)
    _ = x in [1, ClassWithUninferableMeta]
    _ = x in [UnknownHash()]
    _ = x in [BadMRO()]
    _ = x in [DynamicBase()]
    _ = x in [cyclic_tuple]

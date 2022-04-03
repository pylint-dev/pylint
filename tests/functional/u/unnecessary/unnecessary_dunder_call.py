"""Checks for unnecessary-dunder-call."""
# pylint: disable=too-few-public-methods, undefined-variable, useless-object-inheritance
# pylint: disable=missing-class-docstring, missing-function-docstring
from collections import OrderedDict
from typing import Any

# Test includelisted dunder methods raise lint when manually called.
num_str = some_num.__str__() # [unnecessary-dunder-call]
num_repr = some_num.__add__(2) # [unnecessary-dunder-call]
my_repr = my_module.my_object.__repr__() # [unnecessary-dunder-call]

MY_CONTAINS_BAD = {1, 2, 3}.__contains__(1) # [unnecessary-dunder-call]
MY_CONTAINS_GOOD = 1 in {1, 2, 3}

# Just instantiate like a normal person please
my_list_bad = []
my_list_bad.__init__({1, 2, 3}) # [unnecessary-dunder-call]
my_list_good = list({1, 2, 3})

# Test unknown/user-defined dunder methods don't raise lint.
my_woohoo = my_object.__woohoo__()

# Test lint raised within function.
def is_bigger_than_two(val):
    return val.__gt__(2)  # [unnecessary-dunder-call]

# Test dunder methods don't raise lint
# if within a dunder method definition.
class Foo1(object):
    def __init__(self):
        object.__init__(self)

class Foo2(object):
    def __init__(self):
        super().__init__(self)

class Bar1(object):
    def __new__(cls):
        object.__new__(cls)

class Bar2(object):
    def __new__(cls):
        super().__new__(cls)

class CustomRegistry(dict):
    def __init__(self) -> None:
        super().__init__()
        self._entry_ids = {}

    def __setitem__(self, key, entry) -> None:
        super().__setitem__(key, entry)
        self._entry_ids.__setitem__(entry.id, entry)

    def __delitem__(self, key: str) -> None:
        entry = self[key]
        self._entry_ids.__delitem__(entry.id)
        super().__delitem__(key)

class CustomState:
    def __init__(self, state):
        self._state = state

    def __eq__(self, other: Any) -> bool:
        return self._state.__eq__(other)

class CustomDict(OrderedDict):
    def __init__(self, *args, **kwds):
        OrderedDict.__init__(self, *args, **kwds)

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)


class MyClass(list):
    def __contains__(self, item):
        print("do some special checks")
        return super().__contains__(item)

class PluginBase(object):
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

# Allow use of dunder methods that don't
# have an alternate method of being called
class Base:
    @classmethod
    def get_first_subclass(cls):
        for subklass in cls.__subclasses__():
            return subklass
        return object

# Test no lint raised for attributes.
my_instance_name = x.__class__.__name__
my_pkg_version = pkg.__version__

# Allow use of dunder methods on uninstantiated classes
MANUAL_SELF = int.__add__(1, 1)
MY_DICT = {"a": 1, "b": 2}
dict.__setitem__(MY_DICT, "key", "value")

# Still flag instantiated classes
INSTANTIATED_SELF = int("1").__add__(1) # [unnecessary-dunder-call]
{"a": 1, "b": 2}.__setitem__("key", "value") # [unnecessary-dunder-call]

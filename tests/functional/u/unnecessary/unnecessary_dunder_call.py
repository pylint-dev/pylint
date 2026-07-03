"""Checks for unnecessary-dunder-call."""
# pylint: disable=too-few-public-methods, undefined-variable, invalid-name
# pylint: disable=missing-class-docstring, missing-function-docstring
# pylint: disable=protected-access, unnecessary-lambda-assignment, unnecessary-lambda
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
class Foo1:
    def __init__(self):
        object.__init__(self)

class Foo2:
    def __init__(self):
        super().__init__(self)

class Bar1:
    def __new__(cls):
        object.__new__(cls)

class Bar2:
    def __new__(cls):
        super().__new__(cls)

class CustomRegistry(dict):
    def __init__(self) -> None:
        super().__init__()
        self._entry_ids = {}

    def __setitem__(self, key, entry) -> None:
        super().__setitem__(key, entry)
        self._entry_ids.__setitem__(entry.id, entry)
        self._entry_ids.__delitem__(entry.id)

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

class PluginBase:
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

# Validate that dunder call is allowed
# at any depth within dunder definition
class SomeClass:
    def __init__(self):
        self.my_attr = object()

    def __setattr__(self, name, value):
        def nested_function():
            self.my_attr.__setattr__(name, value)

        nested_function()

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

# Allow use of dunder methods on non instantiated classes
MANUAL_SELF = int.__add__(1, 1)
MY_DICT = {"a": 1, "b": 2}
dict.__setitem__(MY_DICT, "key", "value")

# Still flag instantiated classes
INSTANTIATED_SELF = int("1").__add__(1) # [unnecessary-dunder-call]
{"a": 1, "b": 2}.__setitem__("key", "value") # [unnecessary-dunder-call]

# We also exclude dunder methods called on super
# since we can't apply alternate operators/functions here.
a = [1, 2, 3]
assert super(type(a), a).__str__() == "[1, 2, 3]"

class MyString(str):
    """Custom str implementation"""
    def rjust(self, width, fillchar= ' '):
        """Acceptable call to __index__"""
        width = width.__index__()

# Test no lint raised for these dunders within lambdas
lambda1 = lambda x: x.__setitem__(1,2)
lambda2 = lambda x: x.__del__(1)
lambda3 = lambda x,y: x.__ipow__(y)
lambda4 = lambda u,v: u.__setitem__(v())

# Test lint raised for these dunders within lambdas
lambda5 = lambda x: x.__gt__(3) # [unnecessary-dunder-call]
lambda6 = lambda x,y: x.__or__(y) # [unnecessary-dunder-call]
lambda7 = lambda x: x.__iter__() # [unnecessary-dunder-call]
lambda8 = lambda z: z.__hash__() # [unnecessary-dunder-call]
lambda9 = lambda n: (4).__rmul__(n) # [unnecessary-dunder-call]

# pylint: disable=missing-docstring, missing-module-docstring, invalid-name
# pylint: disable=too-few-public-methods, line-too-long, dangerous-default-value
# pylint: disable=wrong-import-order
# https://github.com/pylint-dev/pylint/issues/4774

def github_issue_4774():
    # Test literals
    # https://github.com/pylint-dev/pylint/issues/4774
    good_list = []
    if not good_list:
        pass

    bad_list = []
    if bad_list == []: # [use-implicit-booleaness-not-comparison]
        pass

# Testing for empty literals
empty_tuple = ()
empty_list = []
empty_dict = {}

if empty_tuple == (): # [use-implicit-booleaness-not-comparison]
    pass

if empty_list == []: # [use-implicit-booleaness-not-comparison]
    pass

if empty_dict == {}: # [use-implicit-booleaness-not-comparison]
    pass

if () == empty_tuple: # [use-implicit-booleaness-not-comparison]
    pass

if [] == empty_list: # [use-implicit-booleaness-not-comparison]
    pass

if {} == empty_dict: # [use-implicit-booleaness-not-comparison]
    pass

def bad_tuple_return():
    t = (1, )
    return t == () # [use-implicit-booleaness-not-comparison]

def bad_list_return():
    b = [1]
    return b == [] # [use-implicit-booleaness-not-comparison]

def bad_dict_return():
    c = {1: 1}
    return c == {} # [use-implicit-booleaness-not-comparison]

assert () == empty_tuple # [use-implicit-booleaness-not-comparison]
assert [] == empty_list # [use-implicit-booleaness-not-comparison]
assert {} != empty_dict # [use-implicit-booleaness-not-comparison]
assert () < empty_tuple # [use-implicit-booleaness-not-comparison]
assert [] <= empty_list # [use-implicit-booleaness-not-comparison]
assert () > empty_tuple # [use-implicit-booleaness-not-comparison]
assert [] >= empty_list # [use-implicit-booleaness-not-comparison]

assert empty_list != empty_tuple != {}
assert [] == empty_list == empty_list
assert empty_list != empty_dict != empty_tuple == ()

assert [] == []
assert {} != {}
assert () == ()

d = {}

if d in {}:
    pass

class NoBool:
    def __init__(self):
        self.a = 2

class YesBool:
    def __init__(self):
        self.a = True

    def __bool__(self):
        return self.a


# Should be triggered
a = NoBool()
if [] == a: # [use-implicit-booleaness-not-comparison]
    pass

a = YesBool()
if a == []:
    pass

# compound test cases

e = []
f = {}

if e == [] and f == {}: # [use-implicit-booleaness-not-comparison, use-implicit-booleaness-not-comparison]
    pass


named_fields = [0, "", "42", "forty two"]
empty = any(field == "" for field in named_fields)

something_else = NoBool()
empty_literals = [[], {}, ()]
is_empty = any(field == something_else for field in empty_literals)

h, i, j = 1, None, [1,2,3]

def test(k):
    print(k == {})

def test_with_default(k={}):
    print(k == {})
    print(k == 1)

test(h)
test(i)
test(j)

test_with_default(h)
test_with_default(i)
test_with_default(j)


class A:
    lst = []

    @staticmethod
    def test(b=1):
        print(b)
        return []


if A.lst == []:  # [use-implicit-booleaness-not-comparison]
    pass


if [] == A.lst:  # [use-implicit-booleaness-not-comparison]
    pass


if A.test("b") == []:  # [use-implicit-booleaness-not-comparison]
    pass


def test_function():
    return []


if test_function() == []:  # [use-implicit-booleaness-not-comparison]
    pass

# pylint: disable=import-outside-toplevel, wrong-import-position, import-error
# Numpy has its own implementation of __bool__, but base class has list, that's why the comparison check is happening
import numpy
numpy_array = numpy.array([0])
if numpy_array == []: # [use-implicit-booleaness-not-comparison]
    print('numpy_array')
if numpy_array != []: # [use-implicit-booleaness-not-comparison]
    print('numpy_array')
if numpy_array >= (): # [use-implicit-booleaness-not-comparison]
    print('b')

# pandas has its own implementations of __bool__ and is not subclass of list, dict, or tuple; that's why comparison check is not happening
import pandas as pd
pandas_df = pd.DataFrame()
if pandas_df == []:
    pass
if pandas_df != ():
    pass
if pandas_df <= []:
    print("don't emit warning if variable can't safely be inferred")

from typing import Union
from random import random

var: Union[dict, bool, None] = {}
if random() > 0.5:
    var = True

if var == {}:
    pass

data = {}

if data == {}: # [use-implicit-booleaness-not-comparison]
    print("This will be printed")
if data != {}: # [use-implicit-booleaness-not-comparison]
    print("This will also be printed")

if data or not data:
    print("This however won't be")

# literal string check
long_test = {}
if long_test == {        }: # [use-implicit-booleaness-not-comparison]
    pass


# Check for properties and uninferable class methods
# See https://github.com/pylint-dev/pylint/issues/5646
from xyz import AnotherClassWithProperty


class ParentWithProperty:

    @classmethod
    @property
    def parent_function(cls):
        return {}


class MyClassWithProxy(ParentWithProperty):

    attribute = True

    @property
    @classmethod
    def my_property(cls):
        return {}

    @property
    @classmethod
    def my_difficult_property(cls):
        if cls.attribute:
            return {}
        return MyClassWithProxy()



def test_func():
    """Some assertions against empty dicts."""
    my_class = MyClassWithProxy()
    assert my_class.parent_function == {}  # [use-implicit-booleaness-not-comparison]
    assert my_class.my_property == {}  # [use-implicit-booleaness-not-comparison]

    # If the return value is not always implicit boolean, don't raise
    assert my_class.my_difficult_property == {}
    # Uninferable does not raise
    assert AnotherClassWithProperty().my_property == {}


def test_in_boolean_context():
    """Cases where a comparison like `x != []` is used in a boolean context.

    It is safe and idiomatic to simplify `x != []` to just `x`.
    """
    # pylint: disable=pointless-statement,superfluous-parens,unnecessary-negation

    # Control flow
    if empty_list != []:  # [use-implicit-booleaness-not-comparison]
        pass
    while empty_list != []:  # [use-implicit-booleaness-not-comparison]
        pass
    assert empty_list != []  # [use-implicit-booleaness-not-comparison]

    # Ternary
    _ = 1 if empty_list != [] else 2  # [use-implicit-booleaness-not-comparison]

    # Not
    if not (empty_list != []):  # [use-implicit-booleaness-not-comparison]
        pass

    # Comprehension filters
    [x for x in [] if empty_list != []]  # [use-implicit-booleaness-not-comparison]
    {x for x in [] if empty_list != []}  # [use-implicit-booleaness-not-comparison]
    (x for x in [] if empty_list != [])  # [use-implicit-booleaness-not-comparison]

    # all() / any() with generator expressions
    all(empty_list != [] for _ in range(1))  # [use-implicit-booleaness-not-comparison]
    any(empty_list != [] for _ in range(1))  # [use-implicit-booleaness-not-comparison]

    # filter() with lambda
    filter(lambda: empty_list != [], [])  # [use-implicit-booleaness-not-comparison]

    # boolean cast
    bool(empty_list != [])  # [use-implicit-booleaness-not-comparison]

    # Logical operators nested in boolean contexts
    if empty_list != [] and input():  # [use-implicit-booleaness-not-comparison]
        pass
    while input() or empty_list != []:  # [use-implicit-booleaness-not-comparison]
        pass
    if (empty_list != [] or input()) and input():  # [use-implicit-booleaness-not-comparison]
        pass


def test_not_in_boolean_context():
    """Cases where a comparison like `x != []` is used in a non-boolean context.

    These comparisons cannot be safely replaced with just `x`, and should be explicitly cast using `bool(x)`.
    """
    # pylint: disable=pointless-statement
    _ = empty_list != []  # [use-implicit-booleaness-not-comparison]

    _ = empty_list != [] or input()  # [use-implicit-booleaness-not-comparison]

    print(empty_list != [])  # [use-implicit-booleaness-not-comparison]

    [empty_list != [] for _ in []]  # [use-implicit-booleaness-not-comparison]

    lambda: empty_list != []  # [use-implicit-booleaness-not-comparison]

    filter(lambda x: x, [empty_list != []])  # [use-implicit-booleaness-not-comparison]

    return empty_list != []  # [use-implicit-booleaness-not-comparison]

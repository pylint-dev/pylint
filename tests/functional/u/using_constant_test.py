"""Verify if constant tests are used inside if statements."""
# pylint: disable=invalid-name, missing-docstring,too-few-public-methods
# pylint: disable=expression-not-assigned
# pylint: disable=missing-parentheses-for-call-in-test, unnecessary-comprehension, condition-evals-to-constant
# pylint: disable=use-list-literal, use-dict-literal

import collections


def function():
    yield


class Class:

    def method(self):
        pass


instance = Class()

if collections: # [using-constant-test]
    pass

# GenExpr
if (node for node in range(10)): # [using-constant-test]
    pass

if lambda: None: # [using-constant-test]
    pass

if function: # [using-constant-test]
    pass

if Class: # [using-constant-test]
    pass

if 2: # [using-constant-test]
    pass

if True: # [using-constant-test]
    pass

if '': # [using-constant-test]
    pass

if b'': # [using-constant-test]
    pass

if 2.0: # [using-constant-test]
    pass

if {}: # [using-constant-test]
    pass

if {1, 2, 3}: # [using-constant-test]
    pass

if (1, 2, 3): # [using-constant-test]
    pass

if (): # [using-constant-test]
    pass

if [1, 2, 3]: # [using-constant-test]
    pass

if []: # [using-constant-test]
    pass

# Generator
generator = function()
if generator: # [using-constant-test]
    pass

if 1 if 2 else 3: # [using-constant-test]
    pass

def test_comprehensions():
    [data for data in range(100) if abs] # [using-constant-test]
    [data for data in range(100) if 1] # [using-constant-test]
    (data for data in range(100) if abs) # [using-constant-test]
    (data for data in range(100) if 1) # [using-constant-test]
    {data for data in range(100) if abs} # [using-constant-test]
    {data: 1 for data in range(100) if abs} # [using-constant-test]


# UnboundMethod / Function
if Class.method:  # [using-constant-test]
    pass

# BoundMethod
if instance.method:  # [using-constant-test]
    pass

# For these, we require to do inference, even though the result can be a
# constant value. For some of them, we could determine that the test
# is constant, such as 2 + 3, but the components of the BinOp
# can be anything else (2 + somefunccall).

name = 42
if name:
    pass

if 3 + 4:
    pass

if 3 and 4:
    pass

if not 3:
    pass

if instance.method():
    pass

if 2 < 3:  # [comparison-of-constants]
    pass

if tuple((1, 2, 3)):
    pass

if dict():
    pass

if tuple():
    pass

if list():
    pass

if [1, 2, 3][:1]:
    pass

def test(*args):
    if args:
        return 42
    return None

def test_good_comprehension_checks():
    [data for data in range(100)]
    [data for data in range(100) if data]
    [data for data in range(100) if abs(data)]
    (data for data in range(100) if data)
    (data for data in range(100) if abs(data))
    {data for data in range(100) if data}
    {data for data in range(100) if abs(data)}
    {data: 1 for data in range(100) if data}
    {data: 1 for data in range(100)}


# Calls to functions returning generator expressions are always truthy
def get_generator():
    return (x for x in range(0))

if get_generator():  # [using-constant-test]
    pass

def maybe_get_generator(arg):
    if arg:
        return (x for x in range(0))
    return None

if maybe_get_generator(None):
    pass

y = (a for a in range(10))
if y:  # [using-constant-test]
    pass

z = (a for a in range(10))
z = "red herring"
if z:
    pass

gen = get_generator()
if gen:  # [using-constant-test]
    pass


# Regression test for https://github.com/pylint-dev/pylint/issues/3484
# astroid infers a decorated method as a plain method, whatever the decorator
# does. If the decorator is unknown or a class (such as a third-party
# ``cached_property`` or any other descriptor), the attribute may not be a
# method at all, so the test is not known to be constant.
import uninferable_decorators  # pylint: disable=import-error,wrong-import-position


def plain_decorator(func):
    return func


class Descriptor:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        return self.func(obj)


class DecoratedMethods:
    @uninferable_decorators.cached_property
    def unknown(self):
        return True

    @Descriptor
    def descriptor(self):
        return True

    @plain_decorator
    def decorated(self):
        return True

    @staticmethod
    def static():
        return True

    def check(self):
        if self.unknown:
            pass
        if self.descriptor:
            pass
        if self.decorated:  # [using-constant-test]
            pass
        if self.static:  # [using-constant-test]
            pass


@uninferable_decorators.command
def unknown_decorated_function():
    pass


if unknown_decorated_function:
    pass

# pylint: disable=missing-docstring,no-self-use,too-few-public-methods,wrong-import-position,useless-object-inheritance,use-dict-literal
# pylint: disable=wrong-import-order, undefined-variable

REVISION = None

REVISION() # [not-callable]

def correct():
    return 1

REVISION = correct()

class Correct(object):
    """callable object"""

class MetaCorrect(object):
    """callable object"""
    def __call__(self):
        return self

INSTANCE = Correct()
CALLABLE_INSTANCE = MetaCorrect()
CORRECT = CALLABLE_INSTANCE()
INCORRECT = INSTANCE() # [not-callable]
LIST = []
INCORRECT = LIST() # [not-callable]
DICT = {}
INCORRECT = DICT() # [not-callable]
TUPLE = ()
INCORRECT = TUPLE() # [not-callable]
INT = 1
INCORRECT = INT() # [not-callable]

# Test calling properties. Pylint can detect when using only the
# getter, but it doesn't infer properly when having a getter
# and a setter.
class MyProperty(property):
    """ test subclasses """

class PropertyTest(object):
    """ class """

    def __init__(self):
        self.attr = 4

    @property
    def test(self):
        """ Get the attribute """
        return self.attr

    @test.setter
    def test(self, value):
        """ Set the attribute """
        self.attr = value

    @MyProperty
    def custom(self):
        """ Get the attribute """
        return self.attr

    @custom.setter
    def custom(self, value):
        """ Set the attribute """
        self.attr = value

PROP = PropertyTest()
PROP.test(40) # [not-callable]
PROP.custom() # [not-callable]

# Safe from not-callable when using properties.

class SafeProperty(object):
    @property
    def static(self):
        return staticmethod

    @property
    def klass(self):
        return classmethod

    @property
    def get_lambda(self):
        return lambda: None

    @property
    def other_function(self):
        def function(arg):
            return arg
        return function

    @property
    def dict_builtin(self):
        return dict

    @property
    def range_builtin(self):
        return range

    @property
    def instance(self):
        class Empty(object):
            def __call__(self):
                return 42
        return Empty()

    @property
    def does_not_make_sense(self):
        raise NotImplementedError

PROP1 = SafeProperty()
PROP1.static(2)
PROP1.klass(2)
PROP1.get_lambda()
PROP1.other_function(4)
PROP1.dict_builtin()
PROP1.range_builtin(4)
PROP1.instance()
PROP1.does_not_make_sense()


import missing  # pylint: disable=import-error


class UnknownBaseCallable(missing.Blah):
    pass

UnknownBaseCallable()()

# Regression test for #4426
# If property is inferrable we shouldn't double emit the message
# See: https://github.com/PyCQA/pylint/issues/4426
class ClassWithProperty:
    @property
    def value(self):
        return 42

CLASS_WITH_PROP = ClassWithProperty().value()  # [not-callable]

# Test typing.Namedtuple not callable
# See: https://github.com/PyCQA/pylint/issues/1295
import typing

Named = typing.NamedTuple("Named", [("foo", int), ("bar", int)])
named = Named(1, 2)

# Test descriptor call
def func():
    pass


class ADescriptor:
    def __get__(self, instance, owner):
        return func


class AggregateCls:
    a = ADescriptor()


AggregateCls().a()


# Make sure not-callable isn't raised for descriptors

# astroid can't process descriptors correctly so
# pylint needs to ignore not-callable for them
# right now

# Test for https://github.com/PyCQA/pylint/issues/1699

import multiprocessing

multiprocessing.current_process()

# Make sure not-callable isn't raised for uninferable properties
class MyClass:
    @property
    def call(self):
        return undefined


a = A()
a.call()

# Make sure the callable check does not crash when a node's parent cannot be determined.
def get_number(arg):
    return 2 * arg


get_number(10)()  # [not-callable]

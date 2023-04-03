""" Checks assigning attributes not found in class slots
will trigger assigning-non-slot warning.
"""
# pylint: disable=too-few-public-methods, missing-docstring, import-error, redundant-u-string-prefix, unnecessary-dunder-call
# pylint: disable=attribute-defined-outside-init

from collections import deque

from missing import Unknown

class Empty:
    """ empty """

class Bad:
    """ missing not in slots. """

    __slots__ = ['member']

    def __init__(self):
        self.missing = 42 # [assigning-non-slot]

class Bad2:
    """ missing not in slots """
    __slots__ = [deque.__name__, 'member']

    def __init__(self):
        self.deque = 42
        self.missing = 42 # [assigning-non-slot]

class Bad3(Bad):
    """ missing not found in slots """

    __slots__ = ['component']

    def __init__(self):
        self.component = 42
        self.member = 24
        self.missing = 42 # [assigning-non-slot]
        super().__init__()

class Good(Empty):
    """ missing not in slots, but Empty doesn't
    specify __slots__.
    """
    __slots__ = ['a']

    def __init__(self):
        self.missing = 42

class Good2:
    """ Using __dict__ in slots will be safe. """

    __slots__ = ['__dict__', 'comp']

    def __init__(self):
        self.comp = 4
        self.missing = 5

class PropertyGood:
    """ Using properties is safe. """

    __slots__ = ['tmp', '_value']

    @property
    def test(self):
        return self._value

    @test.setter
    def test(self, value):
        # pylint: disable=attribute-defined-outside-init
        self._value = value

    def __init__(self):
        self.test = 42

class PropertyGood2:
    """ Using properties in the body of the class is safe. """
    __slots__ = ['_value']

    def _getter(self):
        return self._value

    def _setter(self, value):
        # pylint: disable=attribute-defined-outside-init
        self._value = value

    test = property(_getter, _setter)

    def __init__(self):
        self.test = 24

class UnicodeSlots:
    """Using unicode objects in __slots__ is okay.

    On Python 3.3 onward, u'' is equivalent to '',
    so this test should be safe for both versions.
    """
    __slots__ = (u'first', u'second')

    def __init__(self):
        self.first = 42
        self.second = 24


class DataDescriptor:
    def __init__(self, name, default=''):
        self.__name = name
        self.__default = default

    def __get__(self, inst, cls):
        return getattr(inst, self.__name, self.__default)

    def __set__(self, inst, value):
        setattr(inst, self.__name, value)


class NonDataDescriptor:
    def __get__(self, inst, cls):
        return 42


class SlotsWithDescriptor:
    __slots__ = ['_err']
    data_descriptor = DataDescriptor('_err')
    non_data_descriptor = NonDataDescriptor()
    missing_descriptor = Unknown()


def dont_emit_for_descriptors():
    inst = SlotsWithDescriptor()
    # This should not emit, because attr is
    # a data descriptor
    inst.data_descriptor = 'foo'
    inst.non_data_descriptor = 'lala'


class ClassWithSlots:
    __slots__ = ['foobar']


class ClassReassigningDunderClass:
    __slots__ = ['foobar']

    def release(self):
        self.__class__ = ClassWithSlots


class ClassReassingingInvalidLayoutClass:
    __slots__ = []

    def release(self):
        self.__class__ = ClassWithSlots  # [assigning-non-slot]
        self.test = 'test'  # [assigning-non-slot]


# pylint: disable=attribute-defined-outside-init
class ClassHavingUnknownAncestors(Unknown):
    __slots__ = ['yo']

    def test(self):
        self.not_yo = 42


# pylint: disable=wrong-import-order, wrong-import-position
from typing import (
    Generic,
    TypeVar,
)

TypeT = TypeVar('TypeT')


class Cls(Generic[TypeT]):
    """ Simple class with slots """
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


class ClassDefiningSetattr:
    __slots__ = ["foobar"]

    def __init__(self):
        self.foobar = {}

    def __setattr__(self, name, value):
        if name == "foobar":
            super().__setattr__(name, value)
        else:
            self.foobar[name] = value


class ClassWithParentDefiningSetattr(ClassDefiningSetattr):
    __slots__ = []


def dont_emit_for_defined_setattr():
    inst = ClassDefiningSetattr()
    # This should not emit because we can't reason about what happens with
    # classes defining __setattr__
    inst.non_existent = "non-existent"

    child = ClassWithParentDefiningSetattr()
    child.non_existent = "non-existent"

class ColorCls:
    __slots__ = ()
    COLOR = "red"


class Child(ColorCls):
    __slots__ = ()


repro = Child()
Child.COLOR = "blue"

class MyDescriptor:
    """Basic descriptor."""

    def __get__(self, instance, owner):
        return 42

    def __set__(self, instance, value):
        pass


# Regression test from https://github.com/pylint-dev/pylint/issues/6001
class Base:
    __slots__ = ()

    attr2 = MyDescriptor()


class Repro(Base):
    __slots__ = ()


repro = Repro()
repro.attr2 = "anything"

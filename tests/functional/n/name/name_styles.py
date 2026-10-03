"""Test for the invalid-name warning."""
# pylint: disable=unnecessary-pass, unnecessary-comprehension, unused-private-member
# pylint: disable=unnecessary-lambda-assignment
import abc
import collections
import typing
from enum import Enum
from typing import ClassVar

GOOD_CONST_NAME = ''
bad_const_name = 0  # [invalid-name]


def BADFUNCTION_name():  # [invalid-name]
    """Bad function name."""
    BAD_LOCAL_VAR = 1  # [invalid-name]
    print(BAD_LOCAL_VAR)


def func_bad_argname(NOT_GOOD):  # [invalid-name]
    """Function with a badly named argument."""
    return NOT_GOOD


def no_nested_args(arg1, arg21, arg22):
    """Well-formed function."""
    print(arg1, arg21, arg22)


class bad_class_name:  # [invalid-name]
    """Class with a bad name."""


class CorrectClassName:
    """Class with a good name."""

    def __init__(self):
        self._good_private_name = 10
        self.__good_real_private_name = 11
        self.good_attribute_name = 12
        self._Bad_AtTR_name = None  # [invalid-name]
        self.Bad_PUBLIC_name = None  # [invalid-name]

    zz = 'Why Was It Bad Class Attribute?'
    GOOD_CLASS_ATTR = 'Good Class Attribute'

    def BadMethodName(self):  # [invalid-name]
        """A Method with a bad name."""

    def good_method_name(self):
        """A method with a good name."""

    def __DunDER_IS_not_free_for_all__(self):  # [invalid-name]
        """Another badly named method."""


class DerivedFromCorrect(CorrectClassName):
    """A derived class with an invalid inherited members.

    Derived attributes and methods with invalid names do not trigger warnings.
    """
    zz = 'Now a good class attribute'

    def __init__(self):
        super().__init__()
        self._Bad_AtTR_name = None  # Ignored

    def BadMethodName(self):
        """Ignored since the method is in the interface."""


V = [WHAT_Ever_inListComp for WHAT_Ever_inListComp in GOOD_CONST_NAME]

def class_builder():
    """Function returning a class object."""

    class EmbeddedClass:
        """Useless class."""

    return EmbeddedClass

# +1:[invalid-name]
BAD_NAME_FOR_CLASS = collections.namedtuple('Named', ['tuple'])
NEXT_BAD_NAME_FOR_CLASS = class_builder()  # [invalid-name]

GoodName = collections.namedtuple('Named', ['tuple'])
ToplevelClass = class_builder()

# Aliases for classes have the same name constraints.
AlsoCorrect = CorrectClassName
NOT_CORRECT = CorrectClassName  # [invalid-name]


def test_globals():
    """Names in global statements are also checked."""
    global NOT_CORRECT
    global AlsoCorrect
    NOT_CORRECT = 1
    AlsoCorrect = 2


class FooClass:
    """A test case for property names.

    Since by default, the regex for attributes is the same as the one
    for method names, we check the warning messages to contain the
    string 'attribute'.
    """
    @property
    def PROPERTY_NAME(self):  # [invalid-name]
        """Ignored."""
        pass

    @property
    @abc.abstractmethod
    def ABSTRACT_PROPERTY_NAME(self):  # [invalid-name]
        """Ignored."""
        pass

    @PROPERTY_NAME.setter
    def PROPERTY_NAME_SETTER(self):  # [invalid-name]
        """Ignored."""
        pass

    def _nice_and_long_descriptive_private_method_name(self):
        """private method with long name"""
        pass


def good_public_function_name(good_arg_name):
    """This is a perfect public function"""
    good_variable_name = 1
    return good_variable_name + good_arg_name


def _private_scope_function_with_long_descriptive_name():
    """Private scope function are cool with long descriptive names"""
    return 12

LONG_CONSTANT_NAME_IN_PUBLIC_SCOPE_ARE_OKAY = True
good_name_for_funcs = lambda: None
BAD_NAME_FOR_FUNCS = lambda: None  # [invalid-name]
# Non-consts can pass either the variable or const regexes at module-level.
good_name_for_lists = [1, 2, 3]
ALSO_GOOD_FOR_LISTS = [1, 2, 3]

class _AnExceptionalExceptionThatOccursVeryVeryRarely(Exception):
    """A very exceptional exception with a nice descriptive name"""
    pass

class FooEnum(Enum):
    """A test case for enum names."""
    GOOD_ENUM_NAME = 1
    bad_enum_name = 2  # [invalid-name]

class Bar:
    """Class with class variables annotated with ClassVar."""
    CLASS_CONST: ClassVar[int] = 42
    CLASS_CONST2: ClassVar = "const"
    variable: ClassVar[str] = "invalid name"
    CLASS_CONST3: typing.ClassVar
    variable2: typing.ClassVar[int]

"""Tests for annotation of variables and potential use before assignment"""
# pylint: disable=too-few-public-methods, global-variable-not-assigned
from collections import namedtuple
from typing import List

def value_and_type_assignment():
    """The variable assigned a value and type"""
    variable: int = 2
    print(variable)


def only_type_assignment():
    """The variable never gets assigned a value"""
    variable: int
    print(variable)  # [used-before-assignment]


def both_type_and_value_assignment():
    """The variable first gets a type and subsequently a value"""
    variable: int
    variable = 1
    print(variable)


def value_assignment_after_access():
    """The variable gets a value after it has been accessed"""
    variable: int
    print(variable)  # [used-before-assignment]
    variable = 1


def value_assignment_from_iterator():
    """The variables gets a value from an iterator"""
    variable: int
    for variable in (1, 2):
        print(variable)


def assignment_in_comprehension():
    """A previously typed variables gets used in a comprehension. Don't crash!"""
    some_list: List[int]
    some_list = [1, 2, 3]
    some_list = [i * 2 for i in some_list]


def decorator_returning_function():
    """A decorator that returns a wrapper function with decoupled typing"""
    def wrapper_with_decoupled_typing():
        print(var)

    var: int
    var = 2
    return wrapper_with_decoupled_typing


def decorator_returning_incorrect_function():
    """A decorator that returns a wrapper function with decoupled typing"""
    def wrapper_with_type_and_no_value():
        # This emits NameError rather than UnboundLocalError, so
        # undefined-variable is okay, even though the traceback refers
        # to "free variable 'var' referenced before assignment"
        print(var) # [undefined-variable]

    var: int
    return wrapper_with_type_and_no_value


def typing_and_value_assignment_with_tuple_assignment():
    """The typed variables get assigned with a tuple assignment"""
    var_one: int
    var_two: int
    var_one, var_two = 1, 1
    print(var_one)
    print(var_two)


def nested_class_as_return_annotation():
    """A namedtuple as a class attribute is used as a return annotation

    Taken from https://github.com/pylint-dev/pylint/issues/5568"""
    class MyObject:
        """namedtuple as class attribute"""
        Coords = namedtuple('Point', ['x', 'y'])

        def my_method(self) -> Coords:
            """Return annotation is valid"""
            # pylint: disable=unnecessary-pass
            pass

    print(MyObject)

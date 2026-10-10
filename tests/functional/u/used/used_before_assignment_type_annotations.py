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


def conditional_annotated_assignment():
    """Variable is conditionally defined but later used in a type-annotated assignment."""
    if object() is None:
        data={"cat": "harf"}
    token: str = data.get("cat")  # [possibly-used-before-assignment]
    print(token)


def loop_conditional_annotated_assignment():
    """Variable is conditionally defined inside a for-loop but later used
    in a type-annotated assignment.
    """
    for _ in range(3):
        if object() is None:
            data={"cat": "harf"}
    token: str = data.get("cat")  # [possibly-used-before-assignment]
    print(token)


def bare_annotation_except_assignment(text):
    """An except-only assignment need not execute before the later use."""
    error_code: int
    try:
        result = int(text)
    except ValueError:
        error_code = 1
        result = -1
    if result < 0:
        print(error_code)  # [used-before-assignment]


def initialized_annotation_except_assignment(text):
    """An annotated initial value remains available when no exception is raised."""
    error_code: int = 0
    try:
        result = int(text)
    except ValueError:
        error_code = 1
        result = -1
    if result < 0:
        print(error_code)


def bare_annotation_try_finally(text):
    """The assignment may fail before the finally block reads the name."""
    value: int
    try:
        value = int(text)
    finally:
        print(value)  # [used-before-assignment]


def bare_annotation_try_except(text):
    """The assignment may fail before the exception handler reads the name."""
    value: int
    try:
        value = int(text)
    except ValueError:
        print(value)  # [used-before-assignment]


def bare_annotation_try_returns(text):
    """The except assignment executes on every path reaching the later use."""
    value: int
    try:
        return int(text)
    except ValueError:
        value = 0
    return value


def bare_annotation_complete_try_except(text):
    """Both successful conversion and its handler assign a value."""
    value: int
    try:
        value = int(text)
    except ValueError:
        value = 0
    return value


def bare_annotation_if_elif(axis):
    """Preserve existing handling of annotated if/elif assignments."""
    value: int
    if axis == 0:
        value = 0
    elif axis == 1:
        value = 1
    return value


def bare_annotation_if_elif_with_try(text, axis):
    """All branches assign or raise, including a nested exception handler."""
    value: int
    if axis == 0:
        try:
            value = int(text)
        except ValueError:
            value = 0
    elif axis == 1:
        value = 1
    else:
        raise ValueError(axis)
    return value


def bare_annotation_except_with_if_elif(text, axis):
    """An exhaustive conditional inside a handler still need not execute."""
    error_code: int
    try:
        result = int(text)
    except ValueError:
        if axis == 0:
            error_code = 1
        elif axis == 1:
            error_code = 2
        else:
            raise ValueError(axis) from None
        result = -1
    if result < 0:
        print(error_code)  # [used-before-assignment]


def bare_annotation_if_elif_then_except(text, axis):
    """An additional except assignment must not invalidate a prior binding."""
    axis %= 2
    value: int
    if axis == 0:
        value = 0
    elif axis == 1:
        value = 1
    try:
        int(text)
    except ValueError:
        value = 2
    return value

"""Tests for undefined variable with assignment expressions"""
# pylint: disable=using-constant-test, expression-not-assigned

# Tests for annotation of variables and potentially undefinition

from typing import TYPE_CHECKING

def typing_and_assignment_expression():
    """The variable gets assigned in an assignment expression"""
    var: int
    if (var := 1 ** 2):
        print(var)


def typing_and_self_referencing_assignment_expression():
    """The variable gets assigned in an assignment expression that references itself"""
    var: int
    if (var := var ** 2):  # [used-before-assignment]
        print(var)


def self_referencing_assignment_expression():
    """An invalid self-referencing assignment expression"""
    if (var := var()):  # [used-before-assignment]
        print(var)


def typed_assignment_in_function_default(param: str = (typed_default := "walrus")) -> None:
    """An annotated assignment expression in a default parameter should not emit"""
    return param


print(typed_default)


def assignment_in_function_default(param = (default := "walrus")) -> None:
    """An assignment expression in a default parameter should not emit"""
    return param


print(default)


def no_assignment_in_function_default(param: str = "walrus") -> None:
    """No annotated assignment expression should emit"""
    return param


print(no_default) # [undefined-variable]


def no_parameters_in_function_default() -> None:
    """Regression tests for functions without any parameters"""
    return


print(again_no_default) # [undefined-variable]

# Tests for assignment expressions in if ... else comprehensions


[i for i in range(10) if (if_assign_1 := i)]

print(if_assign_1)

IF_TWO = [i for i in range(10) if (if_assign_2 := i)]

print(if_assign_2)

IF_THREE = next(i for i in range(10) if (if_assign_3 := i))

print(if_assign_3)

IF_FOUR = {i: i for i in range(10) if (if_assign_4 := i)}

print(if_assign_4)

IF_FIVE = {i: i if (if_assign_5 := i) else 0 for i in range(10)}
print(if_assign_5)

{i: i if True else (else_assign_1 := i) for i in range(10)}

print(else_assign_1) # [undefined-variable]


# Tests for assignment expressions in the assignment of comprehensions

[(assign_assign_1 := i) for i in range(10)]

print(assign_assign_1)

COMPREHENSION_TWO =[(assign_assign_2 := i) for i in range(10)]

print(assign_assign_2)

COMPREHENSION_THREE = next((assign_assign_3 := i) for i in range(10))

print(assign_assign_3)

COMPREHENSION_FOUR = {i: (assign_assign_4 := i) for i in range(10)}

print(assign_assign_4)

COMPREHENSION_FIVE = {i: (else_assign_2 := i) if False else 0 for i in range(10)}

print(else_assign_2)  # [undefined-variable]


# Tests for assignment expressions in lambda statements

things = []
sorted_things = sorted(
    things,
    key=lambda thing: x_0
    if (x_0 := thing.this_value) < (x_1 := thing.that_value)
    else x_1,
)


# Tests for type annotation reused in comprehension

def type_annotation_used_after_comprehension():
    """https://github.com/pylint-dev/pylint/issues/5326#issuecomment-982635371"""
    my_int: int
    ints = [my_int + 1 for my_int in range(5)]

    for my_int in ints:
        print(my_int)


def type_annotation_unused_after_comprehension():
    """https://github.com/pylint-dev/pylint/issues/5326"""
    my_int: int
    _ = [print(sep=my_int, end=my_int) for my_int in range(10)]


def type_annotation_used_improperly_after_comprehension():
    """https://github.com/pylint-dev/pylint/issues/5654"""
    my_int: int
    _ = [print(sep=my_int, end=my_int) for my_int in range(10)]
    print(my_int)  # [used-before-assignment]


def type_annotation_used_improperly_after_comprehension_2():
    """Same case as above but with positional arguments"""
    my_int: int
    _ = [print(my_int, my_int) for my_int in range(10)]
    print(my_int)  # [used-before-assignment]


# Tests for named expressions (walrus operator)

# Expression in ternary operator: positional argument
print(sep=colon if (colon := ":") else None)


class Dummy:
    """Expression in ternary operator: keyword argument"""
    # pylint: disable=too-few-public-methods
    def __init__(self, value):
        self.value = value


dummy = Dummy(value=val if (val := 'something') else 'anything')

def expression_in_ternary_operator_inside_container():
    """Named expression in ternary operator: inside container"""
    return [val2 if (val2 := 'something') else 'anything']


def expression_in_ternary_operator_inside_container_tuple():
    """Same case, using a tuple inside a 1-element list"""
    return [(val3, val3) if (val3 := 'something') else 'anything']


def expression_in_ternary_operator_inside_container_later_position():
    """
    Named expression follows unrelated item in container.

    If 23 is replaced with `val3`, there is currently a false negative,
    but the false positive here is more important and likely to occur."""
    return [23, val3 if (val3 := 'something') else 'anything']


# Self-referencing
if (z := z):  # [used-before-assignment]
    z = z + 1


if (defined := False):
    NEVER_DEFINED = 1
print(defined)
print(NEVER_DEFINED)  # [used-before-assignment]

if (still_defined := False) == 1:
    NEVER_DEFINED_EITHER = 1
print(still_defined)


if TYPE_CHECKING:
    import enum
    import weakref
elif input():
    if input() + 1:
        pass
    elif (enum := None):
        pass
    else:
        print(None if (weakref := '') else True)
else:
    pass

def defined_by_walrus_in_type_checking() -> weakref:
    """Usage of variables defined in TYPE_CHECKING blocks"""
    print(enum)
    return weakref

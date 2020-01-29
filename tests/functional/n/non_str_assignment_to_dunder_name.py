# pylint: disable=missing-module-docstring, missing-class-docstring
# pylint: disable=too-few-public-methods, missing-function-docstring
# pylint: disable=import-error

import random

from unknown import Unknown


class ExampleClass():
    pass


def example_function():
    pass


def returns_str():
    return "abcd"


def returns_int():
    return 0


def returns_tuple():
    return 0, "abc"


# Might not be thorough if same hash seed is used in testing...
def returns_random_type():
    if random.randint(0, 1) > 0:
        return 0

    return "abc"

ExampleClass.__name__ = 1  # [non-str-assignment-to-dunder-name]
ExampleClass.__name__ = True  # [non-str-assignment-to-dunder-name]
ExampleClass.__name__ = returns_tuple() # [non-str-assignment-to-dunder-name]
ExampleClass.__name__ = returns_int() # [non-str-assignment-to-dunder-name]
ExampleClass.__name__ = "foo"
ExampleClass.__name__ = returns_str()
ExampleClass.__name__ = returns_random_type()
ExampleClass.__name__ = Unknown

example_function.__name__ = 1  # [non-str-assignment-to-dunder-name]
example_function.__name__ = True  # [non-str-assignment-to-dunder-name]
example_function.__name__ = returns_tuple() # [non-str-assignment-to-dunder-name]
example_function.__name__ = returns_int() # [non-str-assignment-to-dunder-name]
example_function.__name__ = "foo"
example_function.__name__ = returns_str()
example_function.__name__ = returns_random_type()
example_function.__name__ = Unknown

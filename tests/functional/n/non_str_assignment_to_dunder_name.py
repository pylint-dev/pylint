# pylint: disable=missing-module-docstring, missing-class-docstring
# pylint: disable=too-few-public-methods, missing-function-docstring


class ExampleClass():
    pass


def example_function():
    pass


ExampleClass.__name__ = 1  # [non-str-assignment-to-dunder-name]
ExampleClass.__name__ = True  # [non-str-assignment-to-dunder-name]
ExampleClass.__name__ = "foo"
example_function.__name__ = 1  # [non-str-assignment-to-dunder-name]
example_function.__name__ = True  # [non-str-assignment-to-dunder-name]
example_function.__name__ = "foo"

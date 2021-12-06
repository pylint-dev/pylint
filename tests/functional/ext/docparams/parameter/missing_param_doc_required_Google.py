"""Tests for missing-param-doc and missing-type-doc for Google style docstrings
with accept-no-param-doc = no

Styleguide:
https://google.github.io/styleguide/pyguide.html#doc-function-args
"""
# pylint: disable=invalid-name, unused-argument, unnecessary-pass, undefined-variable


def test_multi_line_parameters(param: int) -> None:
    """Checks that multi line parameters lists are checked correctly
    See https://github.com/PyCQA/pylint/issues/5452

    Args:
        param:
            a description
    """
    print(param)


def test_missing_func_params_in_google_docstring(  # [missing-param-doc, missing-type-doc]
    x, y, z
):
    """Example of a function with missing Google style parameter
    documentation in the docstring

    Args:
        x: bla
        z (int): bar

    some other stuff
    """
    pass


def test_missing_func_params_with_annotations_in_google_docstring(x: int, y: bool, z):
    """Example of a function with missing Google style parameter
    documentation in the docstring.

        Args:
            x: bla
            y: blah blah
            z (int): bar

        some other stuff
    """
    pass


def test_missing_type_doc_google_docstring_exempt_kwonly_args(
    arg1: int, arg2: int, *, value1: str, value2: str
):
    """Code to show failure in missing-type-doc

    Args:
        arg1: First argument.
        arg2: Second argument.
        value1: First kwarg.
        value2: Second kwarg.
    """
    print("NOTE: It doesn't like anything after the '*'.")


def test_default_arg_with_annotations_in_google_docstring(
    x: int, y: bool, z: int = 786
):
    """Example of a function with missing Google style parameter
        documentation in the docstring.

    Args:
        x: bla
        y: blah blah
        z: bar

    some other stuff
    """
    pass


def test_missing_func_params_with_partial_annotations_in_google_docstring(  # [missing-type-doc]
    x, y: bool, z
):
    """Example of a function with missing Google style parameter
    documentation in the docstring.

    Args:
        x: bla
        y: blah blah
        z (int): bar

    some other stuff
    """
    pass


def test_non_builtin_annotations_in_google_docstring(
    bottomleft: Point, topright: Point
) -> float:
    """Example of a function with missing Google style parameter
    documentation in the docstring.
        Args:
            bottomleft: bottom left point of rectangle
            topright: top right point of rectangle
    """
    pass


def get_midpoint(bottomleft: Point, topright: Point) -> Point:
    """Example of a function with missing Google style parameter
    documentation in the docstring.
    Args:
        bottomleft: bottom left point of rectangle
        topright: top right point of rectangle
    """
    pass


def test_func_params_and_keyword_params_in_google_docstring(this, other, that=True):
    """Example of a function with Google style parameter split
    in Args and Keyword Args in the docstring

        Args:
            this (str): Printed first
            other (int): Other args

        Keyword Args:
            that (bool): Printed second
    """
    print(this, that, other)

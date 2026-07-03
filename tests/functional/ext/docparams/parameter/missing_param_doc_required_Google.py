"""Tests for missing-param-doc and missing-type-doc for Google style docstrings
with accept-no-param-doc = no

Styleguide:
https://google.github.io/styleguide/pyguide.html#doc-function-args
"""

# pylint: disable=invalid-name, unused-argument, undefined-variable
# pylint: disable=line-too-long, too-few-public-methods, missing-class-docstring
# pylint: disable=missing-function-docstring, function-redefined, inconsistent-return-statements
# pylint: disable=dangerous-default-value, too-many-arguments

from __future__ import annotations


def test_multi_line_parameters(param: int) -> None:
    """Checks that multi line parameters lists are checked correctly
    See https://github.com/pylint-dev/pylint/issues/5452

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


def test_missing_func_params_with_annotations_in_google_docstring(x: int, y: bool, z):
    """Example of a function with missing Google style parameter
    documentation in the docstring.

        Args:
            x: bla
            y: blah blah
            z (int): bar

        some other stuff
    """


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


def test_non_builtin_annotations_in_google_docstring(
    bottomleft: Point, topright: Point
) -> float:
    """Example of a function with missing Google style parameter
    documentation in the docstring.
        Args:
            bottomleft: bottom left point of rectangle
            topright: top right point of rectangle
    """


def test_non_builtin_annotations_for_returntype_in_google_docstring(
    bottomleft: Point, topright: Point
) -> Point:
    """Example of a function with missing Google style parameter
    documentation in the docstring.
    Args:
        bottomleft: bottom left point of rectangle
        topright: top right point of rectangle
    """


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


def test_func_params_and_wrong_keyword_params_in_google_docstring(  # [missing-param-doc, missing-type-doc, differing-param-doc, differing-type-doc]
    this, other, that=True
):
    """Example of a function with Google style parameter split
    in Args and Keyword Args in the docstring but with wrong keyword args

        Args:
            this (str): Printed first
            other (int): Other args

        Keyword Args:
            these (bool): Printed second
    """
    print(this, that, other)


class Foo:
    def test_missing_method_params_in_google_docstring(  # [missing-param-doc, missing-type-doc]
        self, x, y
    ):
        """Example of a class method with missing parameter documentation in
        the Google style docstring

        missing parameter documentation

        Args:
            x: bla
        """


def test_existing_func_params_in_google_docstring(xarg, yarg, zarg, warg):
    """Example of a function with correctly documented parameters and
    return values (Google style)

    Args:
        xarg (int): bla xarg
        yarg (my.qualified.type): bla
            bla yarg

        zarg (int): bla zarg
        warg (my.qualified.type): bla warg

    Returns:
        float: sum
    """
    return xarg + yarg


def test_wrong_name_of_func_params_in_google_docstring_one(  # [missing-param-doc, missing-type-doc, differing-param-doc, differing-type-doc]
    xarg, yarg, zarg
):
    """Example of functions with inconsistent parameter names in the
    signature and in the Google style documentation

    Args:
        xarg1 (int): bla xarg
        yarg (float): bla yarg

        zarg1 (str): bla zarg
    """
    return xarg + yarg


def test_wrong_name_of_func_params_in_google_docstring_two(  # [differing-param-doc, differing-type-doc]
    xarg, yarg
):
    """Example of functions with inconsistent parameter names in the
    signature and in the Google style documentation

    Args:
        yarg1 (float): bla yarg

    For the other parameters, see bla.
    """
    return xarg + yarg


def test_see_sentence_for_func_params_in_google_docstring(xarg, yarg):
    """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Google style)

    Args:
        yarg (float): bla yarg

    For the other parameters, see :func:`bla`
    """
    return xarg + yarg


class ClassFoo:  # [missing-param-doc, missing-type-doc]
    """test_constr_params_in_class_google
    Example of a class with missing constructor parameter documentation
    (Google style)

    Everything is completely analogous to functions.

    Args:
        y: bla

    missing constructor parameter documentation
    """

    def __init__(self, x, y):
        pass


class ClassFoo:
    def __init__(self, x, y):  # [missing-param-doc, missing-type-doc]
        """test_constr_params_in_init_google
        Example of a class with missing constructor parameter documentation
        (Google style)

        Args:
            y: bla

        missing constructor parameter documentation
        """


class ClassFoo:  # [multiple-constructor-doc,missing-param-doc, missing-type-doc]
    """test_constr_params_in_class_and_init_google
    Example of a class with missing constructor parameter documentation
    in both the init docstring and the class docstring
    (Google style)

    Everything is completely analogous to functions.

    Args:
        y: bla

    missing constructor parameter documentation
    """

    def __init__(self, x, y):  # [missing-param-doc, missing-type-doc]
        """docstring foo

        Args:
            y: bla

        missing constructor parameter documentation
        """


def test_warns_missing_args_google(named_arg, *args):  # [missing-param-doc]
    """The docstring

    Args:
        named_arg (object): Returned

    Returns:
        object or None: Maybe named_arg
    """
    if args:
        return named_arg


def test_warns_missing_kwargs_google(named_arg, **kwargs):  # [missing-param-doc]
    """The docstring

    Args:
        named_arg (object): Returned

    Returns:
        object or None: Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_finds_args_without_type_google(named_arg, *args):
    """The docstring

    Args:
        named_arg (object): Returned
        *args: Optional arguments

    Returns:
        object or None: Maybe named_arg
    """
    if args:
        return named_arg


def test_finds_kwargs_without_type_google(named_arg, **kwargs):
    """The docstring

    Args:
        named_arg (object): Returned
        **kwargs: Keyword arguments

    Returns:
        object or None: Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_finds_kwargs_without_type_google(named_arg, **kwargs: dict[str, str]):
    """The docstring

    Args:
        named_arg (object): Returned
        **kwargs: Keyword arguments

    Returns:
        object or None: Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_finds_kwargs_without_asterisk_google(named_arg, **kwargs):
    """The docstring

    Args:
        named_arg (object): Returned
        kwargs: Keyword arguments

    Returns:
        object or None: Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_finds_escaped_args_google(value: int, *args: Any) -> None:
    """This is myfunc.

    Args:
        \\*args: this is args
        value: this is value
    """
    print(*args, value)


def test_finds_args_with_xref_type_google(named_arg, **kwargs):
    """The docstring

    Args:
        named_arg (`example.value`): Returned
        **kwargs: Keyword arguments

    Returns:
        `example.value`: Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_ignores_optional_specifier_google(
    param1, param2, param3=(), param4=[], param5=[], param6=True
):  # pylint: disable=too-many-positional-arguments
    """Do something.

    Args:
        param1 (str): Description.
        param2 (dict(str, int)): Description.
        param3 (tuple(str), optional): Defaults to empty. Description.
        param4 (List[str], optional): Defaults to empty. Description.
        param5 (list[tuple(str)], optional): Defaults to empty. Description.
        param6 (bool, optional): Defaults to True. Description.

    Returns:
        int: Description.
    """
    return param1, param2, param3, param4, param5, param6


def test_finds_multiple_complex_types_google(
    named_arg_one,
    named_arg_two,
    named_arg_three,
    named_arg_four,
    named_arg_five,
    named_arg_six,
    named_arg_seven,
    named_arg_eight,
    named_arg_nine,
    named_arg_ten,
):  # pylint: disable=too-many-positional-arguments
    """The google docstring

    Args:
        named_arg_one (dict(str, str)): Returned
        named_arg_two (dict[str, str]): Returned
        named_arg_three (int or str): Returned
        named_arg_four (tuple(int or str)): Returned
        named_arg_five (tuple(int) or list(int)): Returned
        named_arg_six (tuple(int or str) or list(int or str)): Returned
        named_arg_seven (dict(str,str)): Returned
        named_arg_eight (dict[str,str]): Returned
        named_arg_nine (tuple(int)): Returned
        named_arg_ten (list[tokenize.TokenInfo]): Returned

    Returns:
        dict(str, str): named_arg_one
        dict[str, str]: named_arg_two
        int or str: named_arg_three
        tuple(int or str): named_arg_four
        tuple(int) or list(int): named_arg_five
        tuple(int or str) or list(int or str): named_arg_six
        dict(str,str): named_arg_seven
        dict[str,str]: named_arg_eight
        tuple(int): named_arg_nine
        list[tokenize.TokenInfo]: named_arg_ten
    """
    return (
        named_arg_one,
        named_arg_two,
        named_arg_three,
        named_arg_four,
        named_arg_five,
        named_arg_six,
        named_arg_seven,
        named_arg_eight,
        named_arg_nine,
        named_arg_ten,
    )

def test_escape_underscore(something: int, raise_: bool = False) -> bool:
    """Tests param with escaped _ is handled correctly.

    Args:
        something: the something
        raise\\_: the other

    Returns:
        something
    """
    return something and raise_

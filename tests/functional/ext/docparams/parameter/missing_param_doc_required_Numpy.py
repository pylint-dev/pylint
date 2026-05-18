"""Tests for missing-param-doc and missing-type-doc for Numpy style docstrings
with accept-no-param-doc = no
"""

# pylint: disable=invalid-name, unused-argument, undefined-variable, too-many-arguments
# pylint: disable=line-too-long, too-few-public-methods, missing-class-docstring
# pylint: disable=missing-function-docstring, function-redefined, inconsistent-return-statements

from __future__ import annotations


def test_missing_func_params_in_numpy_docstring(  # [missing-param-doc, missing-type-doc]
    x, y, z
):
    """Example of a function with missing NumPy style parameter
        documentation in the docstring

    Parameters
    ----------
    x:
        bla
    z: int
        bar

    some other stuff
    """


class Foo:
    def test_missing_method_params_in_numpy_docstring(  # [missing-param-doc, missing-type-doc]
        self, x, y
    ):
        """Example of a class method with missing parameter documentation in
        the Numpy style docstring

        missing parameter documentation

        Parameters
        ----------
        x:
            bla
        """


def test_existing_func_params_in_numpy_docstring(xarg, yarg, zarg, warg):
    """Example of a function with correctly documented parameters and
    return values (Numpy style)

    Parameters
    ----------
    xarg: int
        bla xarg
    yarg: my.qualified.type
        bla yarg

    zarg: int
        bla zarg
    warg: my.qualified.type
        bla warg

    Returns
    -------
    float
        sum
    """
    return xarg + yarg


def test_wrong_name_of_func_params_in_numpy_docstring(  # [missing-param-doc, missing-type-doc, differing-param-doc, differing-type-doc]
    xarg, yarg, zarg
):
    """Example of functions with inconsistent parameter names in the
    signature and in the Numpy style documentation

    Parameters
    ----------
    xarg1: int
        bla xarg
    yarg: float
        bla yarg

    zarg1: str
        bla zarg
    """
    return xarg + yarg


def test_wrong_name_of_func_params_in_numpy_docstring_two(  # [differing-param-doc, differing-type-doc]
    xarg, yarg
):
    """Example of functions with inconsistent parameter names in the
    signature and in the Numpy style documentation

    Parameters
    ----------
    yarg1: float
        bla yarg

    For the other parameters, see bla.
    """
    return xarg + yarg


def test_see_sentence_for_func_params_in_numpy_docstring(xarg, yarg):
    """Example for the usage of "For the other parameters, see" to avoid
    too many repetitions, e.g. in functions or methods adhering to a
    given interface (Numpy style)

    Parameters
    ----------
    yarg: float
        bla yarg

    For the other parameters, see :func:`bla`
    """
    return xarg + yarg


class ClassFoo:  # [missing-param-doc, missing-type-doc]
    """test_constr_params_in_class_numpy
    Example of a class with missing constructor parameter documentation
    (Numpy style)

    Everything is completely analogous to functions.

    Parameters
    ----------
    y:
        bla

    missing constructor parameter documentation
    """

    def __init__(self, x, y):
        pass


class ClassFoo:
    """test_constr_params_and_attributes_in_class_numpy
    Example of a class with correct constructor parameter documentation
    and an attributes section (Numpy style)

    Parameters
    ----------
    foobar : str
        Something.

    Attributes
    ----------
    barfoor : str
        Something.
    """

    def __init__(self, foobar):
        self.barfoo = None


class ClassFoo:
    def __init__(self, x, y):  # [missing-param-doc, missing-type-doc]
        """test_constr_params_in_init_numpy
        Example of a class with missing constructor parameter documentation
        (Numpy style)

        Everything is completely analogous to functions.

        Parameters
        ----------
        y:
            bla

        missing constructor parameter documentation
        """


class ClassFoo:  # [multiple-constructor-doc, missing-param-doc, missing-type-doc]
    """test_constr_params_in_class_and_init_numpy
    Example of a class with missing constructor parameter documentation
    in both the init docstring and the class docstring
    (Numpy style)

    Everything is completely analogous to functions.

    Parameters
    ----------
    y:
        bla

    missing constructor parameter documentation
    """

    def __init__(self, x, y):  # [missing-param-doc, missing-type-doc]
        """docstring foo

        Parameters
        ----------
        y:
            bla

        missing constructor parameter documentation
        """


def test_warns_missing_args_numpy(named_arg, *args):  # [missing-param-doc]
    """The docstring

    Args
    ----
    named_arg : object
        Returned

    Returns
    -------
        object or None
            Maybe named_arg
    """
    if args:
        return named_arg


def test_warns_missing_kwargs_numpy(named_arg, **kwargs):  # [missing-param-doc]
    """The docstring

    Args
    ----
    named_arg : object
        Returned

    Returns
    -------
        object or None
            Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_finds_args_without_type_numpy(  # [missing-type-doc]
    named_arg, typed_arg: bool, untyped_arg, *args
):
    """The docstring

    Args
    ----
    named_arg : object
        Returned
    typed_arg
        Other argument without numpy type annotation
    untyped_arg
        Other argument without any type annotation
    *args :
        Optional Arguments

    Returns
    -------
        object or None
            Maybe named_arg
    """
    if args:
        return named_arg


def test_finds_args_with_xref_type_numpy(named_arg, *args):
    """The docstring

    Args
    ----
    named_arg : `example.value`
        Returned
    *args :
        Optional Arguments

    Returns
    -------
        `example.value`
            Maybe named_arg
    """
    if args:
        return named_arg


def test_finds_kwargs_without_type_numpy(named_arg, **kwargs):
    """The docstring

    Args
    ----
    named_arg : object
        Returned
    **kwargs :
        Keyword arguments

    Returns
    -------
        object or None
            Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_finds_kwargs_with_type_numpy(named_arg, **kwargs: dict[str, str]):
    """The docstring

    Args
    ----
    named_arg : object
        Returned
    **kwargs :
        Keyword arguments

    Returns
    -------
        object or None
            Maybe named_arg
    """
    if kwargs:
        return named_arg


def test_finds_kwargs_without_asterisk_numpy(named_arg, **kwargs):
    """The docstring

    Args
    ----
    named_arg : object
        Returned
    kwargs :
        Keyword arguments

    Returns
    -------
        object or None
            Maybe named_arg
    """
    if kwargs:
        return named_arg


def my_func(
    named_arg_one,
    named_arg_two,
    named_arg_three,
    named_arg_four,
    named_arg_five,
    named_arg_six,
    named_arg_seven,
    named_arg_eight,
):  # pylint: disable=too-many-positional-arguments
    """The docstring

    Args
    ----
    named_arg_one : dict(str,str)
        Returned
    named_arg_two : dict[str,str]
        Returned
    named_arg_three : tuple(int)
        Returned
    named_arg_four : list[tokenize.TokenInfo]
        Returned
    named_arg_five : int or str
        Returned
    named_arg_six : tuple(int or str)
        Returned
    named_arg_seven : tuple(int) or list(int)
        Returned
    named_arg_eight : tuple(int or str) or list(int or str)
        Returned

    Returns
    -------
        dict(str,str)
            named_arg_one
        dict[str,str]
            named_arg_two
        tuple(int)
            named_arg_three
        list[tokenize.TokenInfo]
            named_arg_four
        int or str
            named_arg_five
        tuple(int or str)
            named_arg_six
        tuple(int) or list(int)
            named_arg_seven
        tuple(int or str) or list(int or str)
            named_arg_eight
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
    )


def test_ignores_optional_specifier_numpy(param, param2="all"):
    """Do something.

    Parameters
    ----------
    param : str
        Description.
    param2 : str, optional
        Description (the default is 'all').

    Returns
    -------
    int
        Description.
    """
    return param, param2


def test_with_list_of_default_values(arg, option, option2):
    """Reported in https://github.com/pylint-dev/pylint/issues/4035.

    Parameters
    ----------
    arg : int
        The number of times to print it.
    option : {"y", "n"}
        Do I do it?
    option2 : {"y", None, "n"}
        Do I do it?

    """
    return arg, option, option2


def test_with_descriptions_instead_of_typing(arg, axis, option):
    """We choose to accept description in place of typing as well.

    See: https://github.com/pylint-dev/pylint/pull/7398.

    Parameters
    ----------
    arg : a number type.
    axis : int or None
    option : {"y", "n"}
        Do I do it?
    """
    return arg, option

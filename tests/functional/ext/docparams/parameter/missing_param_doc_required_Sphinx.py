"""Tests for missing-param-doc and missing-type-doc for Sphinx style docstrings
with accept-no-param-doc = no"""

# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-class-docstring
# pylint: disable=unused-argument, too-few-public-methods, unnecessary-pass, line-too-long
# pylint: disable=missing-function-docstring, disallowed-name

from __future__ import annotations


def test_missing_func_params_in_sphinx_docstring(  # [missing-param-doc, missing-type-doc]
    x, y, z
):
    """Example of a function with missing Sphinx parameter documentation in
    the docstring

    :param x: bla

    :param int z: bar
    """
    pass


class Foo:
    def test_missing_method_params_in_sphinx_docstring(  # [missing-param-doc, missing-type-doc]
        self, x, y
    ):
        """Example of a class method with missing parameter documentation in
        the Sphinx style docstring

        missing parameter documentation

        :param x: bla
        """
        pass


def test_existing_func_params_in_sphinx_docstring(xarg, yarg, zarg, warg):
    """Example of a function with correctly documented parameters and
    return values (Sphinx style)

    :param xarg: bla xarg
    :type xarg: int

    :parameter yarg: bla yarg
    :type yarg: my.qualified.type

    :arg int zarg: bla zarg

    :keyword my.qualified.type warg: bla warg

    :return: sum
    :rtype: float
    """
    return xarg + yarg


def test_wrong_name_of_func_params_in_sphinx_docstring(  # [missing-param-doc, missing-type-doc, differing-param-doc, differing-type-doc]
    xarg, yarg, zarg
):
    """Example of functions with inconsistent parameter names in the
        signature and in the Sphinx style documentation

    :param xarg1: bla xarg
    :type xarg: int

    :param yarg: bla yarg
    :type yarg1: float

    :param str zarg1: bla zarg
    """
    return xarg + yarg


def test_wrong_name_of_func_params_in_sphinx_docstring_two(  # [differing-param-doc, differing-type-doc]
    xarg, yarg, zarg
):
    """Example of functions with inconsistent parameter names in the
        signature and in the Sphinx style documentation

    :param yarg1: bla yarg
    :type yarg1: float

    For the other parameters, see bla.
    """
    return xarg + yarg


def test_see_sentence_for_func_params_in_sphinx_docstring(xarg, yarg) -> None:
    """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Sphinx style)

    :param yarg: bla yarg
    :type yarg: float

    For the other parameters, see :func:`bla`
    """
    return xarg + yarg


class ClassFoo:  # [missing-param-doc, missing-type-doc]
    """test_constr_params_in_class_sphinx
    Example of a class with missing constructor parameter documentation
    (Sphinx style)

    Everything is completely analogous to functions.

    :param y: bla

    missing constructor parameter documentation
    """

    def __init__(self, x, y):
        pass


class ClassFoo:
    def __init__(self, x, y):  # [missing-param-doc, missing-type-doc]
        """test_constr_params_in_init_sphinx
        Example of a class with missing constructor parameter documentation
        (Sphinx style)

        Everything is completely analogous to functions.

        :param y: bla

        missing constructor parameter documentation
        """

        pass


class ClassFoo:  # [multiple-constructor-doc, missing-param-doc, missing-type-doc]
    """test_constr_params_in_class_and_init_sphinx
    Example of a class with missing constructor parameter documentation
    in both the init docstring and the class docstring
    (Sphinx style)

    Everything is completely analogous to functions.

    :param y: None

    missing constructor parameter documentation
    """

    def __init__(self, x, y):  # [missing-param-doc, missing-type-doc]
        """docstring foo

        :param y: bla

        missing constructor parameter documentation
        """
        pass


def test_warns_missing_args_sphinx(  # [missing-param-doc, inconsistent-return-statements]
    named_arg, *args
):
    """The docstring

    :param named_arg: Returned
    :type named_arg: object

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if args:
        return named_arg


def test_warns_missing_kwargs_sphinx(  # [missing-param-doc, inconsistent-return-statements]
    named_arg, **kwargs
):
    """The docstring

    :param named_arg: Returned
    :type named_arg: object

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if kwargs:
        return named_arg


def test_warns_typed_kwargs_sphinx(  # [missing-param-doc, inconsistent-return-statements]
    named_arg, **kwargs: dict[str, str]
):
    """The docstring

    :param named_arg: Returned
    :type named_arg: object

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if kwargs:
        return named_arg


def test_finds_args_without_type_sphinx(  # [missing-param-doc, inconsistent-return-statements]
    named_arg, *args
):
    """The docstring

    :param named_arg: Returned
    :type named_arg: object

    :param *args: Optional arguments

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if args:
        return named_arg


def test_finds_kwargs_without_type_sphinx(  # [missing-param-doc, inconsistent-return-statements]
    named_arg, **kwargs
):
    """The docstring

    :param named_arg: Returned
    :type named_arg: object

    :param **kwargs: Keyword arguments

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if kwargs:
        return named_arg


def test_finds_args_without_type_sphinx(  # [inconsistent-return-statements]
    named_arg, *args
):
    r"""The Sphinx docstring
    In Sphinx docstrings asterisks should be escaped.
    See https://github.com/pylint-dev/pylint/issues/5406

    :param named_arg: Returned
    :type named_arg: object

    :param \*args: Optional arguments

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if args:
        return named_arg


def test_finds_kwargs_without_type_sphinx(  # [inconsistent-return-statements]
    named_arg, **kwargs
):
    r"""The Sphinx docstring
    In Sphinx docstrings asterisks should be escaped.
    See https://github.com/pylint-dev/pylint/issues/5406

    :param named_arg: Returned
    :type named_arg: object

    :param \**kwargs: Keyword arguments

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if kwargs:
        return named_arg


def test_finds_args_without_type_sphinx(  # [inconsistent-return-statements]
    named_arg, *args
):
    r"""The Sphinx docstring
    We can leave the asterisk out.

    :param named_arg: Returned
    :type named_arg: object

    :param args: Optional arguments

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if args:
        return named_arg


def test_finds_kwargs_without_type_sphinx(  # [inconsistent-return-statements]
    named_arg, **kwargs
):
    r"""The Sphinx docstring
    We can leave the asterisk out.

    :param named_arg: Returned
    :type named_arg: object

    :param kwargs: Keyword arguments

    :returns: Maybe named_arg
    :rtype: object or None
    """
    if kwargs:
        return named_arg


class Foo:
    """test_finds_missing_raises_from_setter_sphinx
    Example of a setter having missing raises documentation in
    the Sphinx style docstring of the property
    """

    @property
    def foo(self):  # [missing-raises-doc]
        """docstring ...

        :type: int
        """
        return 10

    @foo.setter
    def foo(self, value):
        raise AttributeError()


class Foo:
    """test_finds_missing_raises_in_setter_sphinx
    Example of a setter having missing raises documentation in
    its own Sphinx style docstring
    """

    @property
    def foo(self):
        """docstring ...

        :type: int
        :raises RuntimeError: Always
        """
        raise RuntimeError()
        return 10  # [unreachable]

    @foo.setter
    def foo(self, value):  # [missing-raises-doc, missing-param-doc, missing-type-doc]
        """setter docstring ...

        :type: None
        """
        raise AttributeError()


class Foo:
    """test_finds_property_return_type_sphinx
    Example of a property having return documentation in
    a Sphinx style docstring
    """

    @property
    def foo(self):
        """docstring ...

        :type: int
        """
        return 10


class Foo:
    """test_finds_annotation_property_return_type_sphinx
    Example of a property having missing return documentation in
    a Sphinx style docstring
    """

    @property
    def foo(self) -> int:
        """docstring ...

        :raises RuntimeError: Always
        """
        raise RuntimeError()
        return 10  # [unreachable]


class Foo:
    def test_useless_docs_ignored_argument_names_sphinx(  # [useless-type-doc, useless-param-doc]
        self, arg, _, _ignored
    ):
        """Example of a method documenting the return type that an
        implementation should return.

        :param arg: An argument.
        :type arg: int

        :param _: Another argument.
        :type _: float

        :param _ignored: Ignored argument.
        """
        pass


def test_finds_multiple_types_sphinx_one(named_arg):
    """The Sphinx docstring

    :param named_arg: Returned
    :type named_arg: dict(str, str)

    :returns: named_arg
    :rtype: dict(str, str)
    """
    return named_arg


def test_finds_multiple_types_sphinx_two(named_arg):
    """The Sphinx docstring

    :param named_arg: Returned
    :type named_arg: dict[str, str]

    :returns: named_arg
    :rtype: dict[str, str]
    """
    return named_arg


def test_finds_multiple_types_sphinx_three(named_arg):
    """The Sphinx docstring

    :param named_arg: Returned
    :type named_arg: int or str

    :returns: named_arg
    :rtype: int or str
    """
    return named_arg


def test_finds_multiple_types_sphinx_four(named_arg):
    """The Sphinx docstring

    :param named_arg: Returned
    :type named_arg: tuple(int or str)

    :returns: named_arg
    :rtype: tuple(int or str)
    """
    return named_arg


def test_finds_multiple_types_sphinx_five(named_arg):
    """The Sphinx docstring

    :param named_arg: Returned
    :type named_arg: tuple(int) or list(int)

    :returns: named_arg
    :rtype: tuple(int) or list(int)
    """
    return named_arg


def test_finds_multiple_types_sphinx_six(named_arg):
    """The Sphinx docstring

    :param named_arg: Returned
    :type named_arg: tuple(int or str) or list(int or str)

    :returns: named_arg
    :rtype: tuple(int or str) or list(int or str)
    """
    return named_arg


def test_finds_compact_container_types_sphinx_one(named_arg):
    """The Sphinx docstring

    :param dict(str,str) named_arg: Returned

    :returns: named_arg
    :rtype: dict(str,str)
    """
    return named_arg


def test_finds_compact_container_types_sphinx_two(named_arg):
    """The Sphinx docstring

    :param dict[str,str] named_arg: Returned

    :returns: named_arg
    :rtype: dict[str,str]
    """
    return named_arg


def test_finds_compact_container_types_sphinx_three(named_arg):
    """The Sphinx docstring

    :param tuple(int) named_arg: Returned

    :returns: named_arg
    :rtype: tuple(int)
    """
    return named_arg


def test_finds_compact_container_types_sphinx_four(named_arg):
    """The Sphinx docstring

    :param list[tokenize.TokenInfo] named_arg: Returned

    :returns: named_arg
    :rtype: list[tokenize.TokenInfo]
    """
    return named_arg

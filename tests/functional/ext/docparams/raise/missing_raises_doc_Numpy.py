"""Tests for missing-raises-doc and missing-raises-type-doc for Numpy style docstrings

Styleguide:
https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, try-except-raise, import-outside-toplevel
# pylint: disable=too-few-public-methods, disallowed-name, using-constant-test


def test_find_missing_numpy_raises(self):  # [missing-raises-doc]
    """This is a Numpy docstring.

    Raises
    ------
    NameError
        Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_all_numpy_raises(self):
    """This is a Numpy docstring.

    Raises
    ------
    RuntimeError
        Always
    NameError
        Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_rethrown_numpy_raises(self):  # [missing-raises-doc]
    """This is a Numpy docstring.

    Raises
    ------
    NameError
        Sometimes
    """
    try:
        fake_func()
    except RuntimeError:
        raise

    raise NameError("hi")


def test_find_rethrown_numpy_multiple_raises(self):  # [missing-raises-doc]
    """This is a Numpy docstring.

    Raises
    ------
    NameError
        Sometimes
    """
    try:
        fake_func()
    except (RuntimeError, ValueError):
        raise

    raise NameError("hi")


def test_ignores_caught_numpy_raises(self):
    """This is a numpy docstring.

    Raises
    ------
    NameError
        Sometimes
    """
    try:
        raise RuntimeError("hi")
    except RuntimeError:
        pass

    raise NameError("hi")


def test_find_numpy_attr_raises_exact_exc(self):
    """This is a numpy docstring.

    Raises
    ------
    calendar.IllegalMonthError
        Sometimes
    """
    import calendar

    raise calendar.IllegalMonthError(-1)


def test_find_numpy_attr_raises_substr_exc(self):
    """This is a numpy docstring.

    Raises
    ------
    calendar.IllegalMonthError
        Sometimes
    """
    from calendar import IllegalMonthError

    raise IllegalMonthError(-1)


def test_find_valid_missing_numpy_attr_raises(self):  # [missing-raises-doc]
    """This is a numpy docstring.

    Raises
    ------
    calendar.anothererror
        Sometimes
    """
    from calendar import IllegalMonthError

    raise IllegalMonthError(-1)


def test_find_invalid_missing_numpy_attr_raises(self):
    """This is a numpy docstring.
     pylint allows this to pass since the comparison between Raises and
    raise are based on the class name, not the qualified name.

    Raises
    ------
    bogusmodule.error
        Sometimes
    """
    from re import error

    raise error("hi")


class Foo:
    """test_finds_missing_raises_from_setter_numpy
    Example of a setter having missing raises documentation in
    the Numpy style docstring of the property
    """

    @property
    def foo(self):  # [missing-raises-doc]
        """int: docstring

        Include a "Raises" section so that this is identified
        as a Numpy docstring and not a Google docstring.

        Raises
        ------
        RuntimeError
            Always
        """
        raise RuntimeError()
        return 10  # [unreachable]

    @foo.setter
    def foo(self, value):
        print(self)
        raise AttributeError()


class Foo:
    """test_finds_missing_raises_from_setter_numpy_2
    Example of a setter having missing raises documentation in
    its own Numpy style docstring of the property
    """

    @property
    def foo(self):
        """int: docstring ...

        Raises
        ------
        RuntimeError
            Always
        """
        raise RuntimeError()
        return 10  # [unreachable]

    @foo.setter
    def foo(self, value):  # [missing-raises-doc]
        """setter docstring ...

        Raises
        ------
        RuntimeError
            Never
        """
        print(self)
        if True:
            raise AttributeError()
        raise RuntimeError()


class Foo:
    """test_finds_property_return_type_numpy
    Example of a property having return documentation in
    a numpy style docstring
    """

    @property
    def foo(self):
        """int: docstring ...

        Raises
        ------
        RuntimeError
            Always
        """
        raise RuntimeError()
        return 10  # [unreachable]

"""Tests for missing-raises-doc and missing-raises-type-doc for Google style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-outside-toplevel, import-error, try-except-raise, too-few-public-methods


def test_find_missing_google_raises(self):  # [missing-raises-doc]
    """This is a Google docstring.

    Raises:
        NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_google_attr_raises_exact_exc(self):
    """This is a google docstring.

    Raises:
        calendar.IllegalMonthError: Sometimes
    """
    import calendar

    raise calendar.IllegalMonthError(-1)


def test_find_google_attr_raises_substr_exc(self):
    """This is a google docstring.

    Raises:
        calendar.IllegalMonthError: Sometimes
    """
    from calendar import IllegalMonthError

    raise IllegalMonthError(-1)


def test_find_valid_missing_google_attr_raises(self):  # [missing-raises-doc]
    """This is a google docstring.

    Raises:
        calendar.anothererror: Sometimes
    """
    from calendar import IllegalMonthError

    raise IllegalMonthError(-1)


def test_find_invalid_missing_google_attr_raises(self):
    """This is a google docstring.
    pylint allows this to pass since the comparison between Raises and
    raise are based on the class name, not the qualified name.

    Raises:
        bogusmodule.error: Sometimes
    """
    from re import error

    raise error("hi")


def test_google_raises_local_reference(self):
    """This is a google docstring.
    pylint allows this to pass since the comparison between Raises and
    raise are based on the class name, not the qualified name.

    Raises:
        .LocalException: Always
    """
    from neighbor_module import LocalException

    raise LocalException("hi")


def test_find_all_google_raises(self):
    """This is a Google docstring.

    Raises:
        RuntimeError: Always
        NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_multiple_google_raises(self):
    """This is a Google docstring.

    Raises:
        RuntimeError: Always
        NameError, OSError, ValueError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]
    raise OSError(2, "abort!")  # [unreachable]
    raise ValueError("foo")  # [unreachable]


def test_find_rethrown_google_raises(self):  # [missing-raises-doc]
    """This is a Google docstring.

    Raises:
        NameError: Sometimes
    """
    try:
        fake_func()
    except RuntimeError:
        raise

    raise NameError("hi")


def test_find_rethrown_google_multiple_raises(self):  # [missing-raises-doc]
    """This is a Google docstring.

    Raises:
        NameError: Sometimes
    """
    try:
        fake_func()
    except (RuntimeError, ValueError):
        raise

    raise NameError("hi")


def test_ignores_caught_google_raises(self):
    """This is a Google docstring.

    Raises:
        NameError: Sometimes
    """
    try:
        raise RuntimeError("hi")
    except RuntimeError:
        pass

    raise NameError("hi")


class Foo:
    """test_finds_missing_raises_from_setter_google
    Example of a setter having missing raises documentation in
    the Google style docstring of the property
    """

    @property
    def foo_method(self):  # [missing-raises-doc]
        """int: docstring

        Include a "Raises" section so that this is identified
        as a Google docstring and not a Numpy docstring.

        Raises:
            RuntimeError: Always
        """
        raise RuntimeError()
        return 10  # [unreachable]

    @foo_method.setter
    def foo_method(self, value):
        print(self)
        raise AttributeError()


class Foo:
    """test_finds_missing_raises_from_setter_google_2
    Example of a setter having missing raises documentation in
    its own Google style docstring of the property.
    """

    @property
    def foo_method(self):
        """int: docstring ...

        Raises:
            RuntimeError: Always
        """
        raise RuntimeError()
        return 10  # [unreachable]

    @foo_method.setter
    def foo_method(self, value):  # [missing-raises-doc]
        """setter docstring ...

        Raises:
            RuntimeError: Never
        """
        print(self)
        if True:  # [using-constant-test]
            raise AttributeError()
        raise RuntimeError()

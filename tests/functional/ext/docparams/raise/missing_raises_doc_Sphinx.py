"""Tests for missing-raises-doc and missing-raises-type-doc for Sphinx style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, try-except-raise, import-outside-toplevel
# pylint: disable=missing-class-docstring, too-few-public-methods


def test_find_missing_sphinx_raises(self):  # [missing-raises-doc]
    """This is a Sphinx docstring.

    :raises NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_ignore_spurious_sphinx_raises(self):
    """This is a Sphinx docstring.

    :raises RuntimeError: Always
    :except NameError: Never
    :raise OSError: Never
    :exception ValueError: Never
    """
    raise RuntimeError("Blah")


def test_find_all_sphinx_raises(self):
    """This is a Sphinx docstring.

    :raises RuntimeError: Always
    :except NameError: Never
    :raise OSError: Never
    :exception ValueError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]
    raise OSError(2, "abort!")  # [unreachable]
    raise ValueError("foo")  # [unreachable]


def test_find_multiple_sphinx_raises(self):
    """This is a Sphinx docstring.

    :raises RuntimeError: Always
    :raises NameError, OSError, ValueError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_finds_rethrown_sphinx_raises(self):  # [missing-raises-doc]
    """This is a Sphinx docstring.

    :raises NameError: Sometimes
    """
    try:
        fake_func()
    except RuntimeError:
        raise

    raise NameError("hi")


def test_finds_rethrown_sphinx_multiple_raises(self):  # [missing-raises-doc]
    """This is a Sphinx docstring.

    :raises NameError: Sometimes
    """
    try:
        fake_func()
    except (RuntimeError, ValueError):
        raise

    raise NameError("hi")


def test_ignores_caught_sphinx_raises(self):
    """This is a Sphinx docstring.

    :raises NameError: Sometimes
    """
    try:
        raise RuntimeError("hi")
    except RuntimeError:
        pass

    raise NameError("hi")


def test_find_missing_sphinx_raises_infer_from_instance(self):  # [missing-raises-doc]
    """This is a Sphinx docstring.

    :raises NameError: Never
    """
    my_exception = RuntimeError("hi")
    raise my_exception
    raise NameError("hi")  # [unreachable]


def test_find_missing_sphinx_raises_infer_from_function(self):  # [missing-raises-doc]
    """This is a Sphinx docstring.

    :raises NameError: Never
    """

    def ex_func(val):
        return RuntimeError(val)

    raise ex_func("hi")
    raise NameError("hi")  # [unreachable]


def test_find_sphinx_attr_raises_exact_exc(self):
    """This is a sphinx docstring.

    :raises re.error: Sometimes
    """
    import re

    raise re.error("hi")


def test_find_sphinx_attr_raises_substr_exc(self):
    """This is a sphinx docstring.

    :raises calendar.IllegalMonthError: Sometimes
    """
    from calendar import IllegalMonthError

    raise IllegalMonthError(-1)


def test_find_valid_missing_sphinx_attr_raises(self):  # [missing-raises-doc]
    """This is a sphinx docstring.

    :raises calendar.anothererror: Sometimes
    """
    from calendar import IllegalMonthError

    raise IllegalMonthError(-1)


def test_find_invalid_missing_sphinx_attr_raises(self):
    """This is a sphinx docstring.
    pylint allows this to pass since the comparison between Raises and
    raise are based on the class name, not the qualified name.

    :raises bogusmodule.IllegalMonthError: Sometimes
    """
    from calendar import IllegalMonthError

    raise IllegalMonthError(-1)


class Foo:
    def test_ignores_raise_notimplementederror_sphinx(self, arg):
        """docstring ...

        :param arg: An argument.
        :type arg: int
        """
        raise NotImplementedError()

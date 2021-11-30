"""Tests for missing-raises-doc and missing-raises-type-doc for Sphinx style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, try-except-raise, import-outside-toplevel


def test_find_missing_sphinx_raises(self):  # [missing-raises-doc]
    """This is a docstring.

    :raises NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_ignore_spurious_sphinx_raises(self):
    """This is a docstring.

    :raises RuntimeError: Always
    :except NameError: Never
    :raise OSError: Never
    :exception ValueError: Never
    """
    raise RuntimeError("Blah")


def test_find_all_sphinx_raises(self):
    """This is a docstring.

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
    """This is a docstring.

    :raises RuntimeError: Always
    :raises NameError, OSError, ValueError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_finds_rethrown_sphinx_raises(self):  # [missing-raises-doc]
    """This is a docstring.

    :raises NameError: Sometimes
    """
    try:
        fake_func()
    except RuntimeError:
        raise

    raise NameError("hi")


def test_finds_rethrown_sphinx_multiple_raises(self):  # [missing-raises-doc]
    """This is a docstring.

    :raises NameError: Sometimes
    """
    try:
        fake_func()
    except (RuntimeError, ValueError):
        raise

    raise NameError("hi")


def test_ignores_caught_sphinx_raises(self):
    """This is a docstring.

    :raises NameError: Sometimes
    """
    try:
        raise RuntimeError("hi")
    except RuntimeError:
        pass

    raise NameError("hi")


def test_find_missing_sphinx_raises_infer_from_instance(self):  # [missing-raises-doc]
    """This is a docstring.

    :raises NameError: Never
    """
    my_exception = RuntimeError("hi")
    raise my_exception
    raise NameError("hi")  # [unreachable]


def test_find_missing_sphinx_raises_infer_from_function(self):  # [missing-raises-doc]
    """This is a docstring.

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

    :raises re.error: Sometimes
    """
    from re import error

    raise error("hi")


def test_find_valid_missing_sphinx_attr_raises(self):  # [missing-raises-doc]
    """This is a sphinx docstring.

    :raises re.anothererror: Sometimes
    """
    from re import error

    raise error("hi")

"""Tests for missing-raises-doc and missing-raises-type-doc for Sphinx style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


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

"""Tests for missing-return-doc and missing-return-type-doc for Sphinx style docstrings
with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):  # [missing-return-type-doc]
    """Warn partial sphinx returns

    :returns: Always False
    """
    return False


def my_func(self) -> bool:
    """Sphinx missing return type with annotations

    :returns: Always False
    """
    return False


def my_func(self):  # [missing-return-doc]
    """Warn partial sphinx returns type

    :rtype: bool
    """
    return False


def warn_missing_sphinx_returns(self, doc_type):  # [missing-return-type-doc, missing-return-doc]
    """This is a docstring.

    :param doc_type: Sphinx
    :type doc_type: str
    """
    return False


def my_func(self):  # [missing-return-doc]
    """warns_sphinx_return_list_of_custom_class_without_description

    :rtype: list(:class:`mymodule.Class`)
    """
    return [mymodule.Class()]

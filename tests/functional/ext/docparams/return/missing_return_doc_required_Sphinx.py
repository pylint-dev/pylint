"""Tests for missing-return-doc and missing-return-type-doc for Sphinx style docstrings
with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, disallowed-name, too-few-public-methods
# pylint: disable=line-too-long


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


def warn_missing_sphinx_returns(  # [missing-return-type-doc, missing-return-doc]
    self, doc_type
):
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


class Foo:
    """test_finds_missing_property_return_type_sphinx
    Example of a property having missing return documentation in
    a Sphinx style docstring
    """

    @property
    def foo(self):  # [missing-return-type-doc]
        """docstring ...

        :raises RuntimeError: Always
        """
        raise RuntimeError()
        return 10  # [unreachable]


class Foo:
    """Example of a class function trying to use `type` as return
    documentation in a Sphinx style docstring
    """

    def test_ignores_non_property_return_type_sphinx(  # [missing-return-doc, missing-return-type-doc]
        self,
    ):
        """docstring ...

        :type: int
        """
        return 10

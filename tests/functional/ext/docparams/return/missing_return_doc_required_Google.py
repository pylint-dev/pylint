"""Tests for missing-return-doc and missing-return-type-doc for Google style docstrings
with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):  # [missing-return-type-doc]
    """Warn partial google returns

    Returns:
        Always False
    """
    return False


def my_func(self):  # [missing-return-doc]
    """warn_partial_google_returns_type

    Returns:
        bool:
    """
    return False


def my_func(self, doc_type):  # [missing-return-doc, missing-return-type-doc]
    """warn_missing_google_returns

    Parameters:
        doc_type (str): Google
    """
    return False


def my_func(self):  # [missing-return-doc]
    """warns_google_return_list_of_custom_class_without_description

    Returns:
        list(:class:`mymodule.Class`):
    """
    return [mymodule.Class()]

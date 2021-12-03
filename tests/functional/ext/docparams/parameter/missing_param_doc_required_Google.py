"""Tests for missing-param-doc and missing-type-doc for Google style docstrings
with accept-no-param-doc = no

Styleguide:
https://google.github.io/styleguide/pyguide.html#doc-function-args
"""
# pylint: disable=invalid-name


def test_multi_line_parameters(param: int) -> None:
    """Checks that multi line parameters lists are checked correctly
    See https://github.com/PyCQA/pylint/issues/5452

    Args:
        param:
            a description
    """
    print(param)

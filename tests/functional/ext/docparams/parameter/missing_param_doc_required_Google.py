"""Tests for missing-param-doc and missing-type-doc for Google style docstrings
with accept-no-param-doc = no

Styleguide:
https://google.github.io/styleguide/pyguide.html#doc-function-args
"""
# pylint: disable=invalid-name, unused-argument, unnecessary-pass


def test_multi_line_parameters(param: int) -> None:
    """Checks that multi line parameters lists are checked correctly
    See https://github.com/PyCQA/pylint/issues/5452

    Args:
        param:
            a description
    """
    print(param)


def test_missing_func_params_in_google_docstring(  # [missing-param-doc, missing-type-doc]
    x, y, z
):
    """Example of a function with missing Google style parameter
    documentation in the docstring

    Args:
        x: bla
        z (int): bar

    some other stuff
    """
    pass

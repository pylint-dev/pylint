"""Tests for missing-raises-doc and missing-raises-type-doc with accept-no-raise-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def test_warns_unknown_style(self):  # [missing-raises-doc]
    """This is a docstring."""
    raise RuntimeError("hi")


# This function doesn't require a docstring, because its name starts
# with an '_' (no-docstring-rgx):
def _function(some_arg: int):
    """This is a docstring."""
    raise ValueError

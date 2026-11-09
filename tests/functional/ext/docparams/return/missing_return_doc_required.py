"""Tests for missing-return-doc and missing-return-type-doc with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def warns_no_docstring(self):  # [missing-return-doc, missing-return-type-doc]
    return False


# this function doesn't require a docstring, because its name starts
# with an '_' (no-docstring-rgx):
def _function(some_arg: int) -> int:
    _ = some_arg
    return 0


def warns_once_with_several_returns(value):  # [missing-return-doc, missing-return-type-doc]
    if value is None:
        return None
    if value:
        return True

    def inner():  # [missing-return-doc, missing-return-type-doc]
        return False

    return inner()

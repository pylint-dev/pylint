# pylint: disable=missing-function-docstring, missing-module-docstring
def add(x, y, /):  # [using-positional-only-args-in-unsupported-version]
    return x + y

"""Regression test for https://github.com/pylint-dev/pylint/issues/11312.

The length of an exception's ``args`` is unknown, so unpacking it must not be
reported as unbalanced.
"""

# pylint: disable=missing-function-docstring, missing-class-docstring


def unpack_exception_args():
    try:
        pass
    except ValueError as exc:
        (message,) = exc.args
        first, second = exc.args
        return message, first, second
    return None


class PackageNotFoundError(ModuleNotFoundError):
    @property
    def name(self) -> str:
        (name,) = self.args
        return name

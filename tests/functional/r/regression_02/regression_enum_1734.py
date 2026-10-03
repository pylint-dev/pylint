# Regression test for https://github.com/pylint-dev/astroid/pull/1734
# The following should lint just fine
# Fixed in https://github.com/pylint-dev/astroid/pull/1743

# pylint: disable=missing-docstring,invalid-name

from enum import Enum

class Test(Enum):
    LOADED = "loaded", True
    SETUP_ERROR = "setup_error", True

    _recoverable: bool

    def __new__(cls, value: str, recoverable: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._recoverable = recoverable
        return obj

    @property
    def recoverable(self) -> bool:
        """Get if the state is recoverable."""
        return self._recoverable

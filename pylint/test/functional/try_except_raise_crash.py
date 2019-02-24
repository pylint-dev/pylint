# pylint: disable=missing-docstring,too-many-ancestors, broad-except
import collections.abc
from typing import TYPE_CHECKING, Any, MutableMapping

if TYPE_CHECKING:
    BaseClass = MutableMapping[str, Any]
else:
    BaseClass = collections.abc.MutableMapping


class TestBaseException(BaseClass):
    pass


class TestException(TestBaseException):
    pass


def test():
    try:
        1 / 0
    except TestException:  # [try-except-raise]
        raise
    except Exception:
        pass

# pylint: disable=missing-docstring,too-many-ancestors, broad-except
import collections.abc
from typing import TYPE_CHECKING, Sized  # pylint: disable=deprecated-class

if TYPE_CHECKING:
    BaseClass = Sized
else:
    BaseClass = collections.abc.Sized


class TestBaseException(BaseClass):
    def __len__(self):
        return 0


class TestException(TestBaseException):
    pass


def test():
    try:
        1 / 0
    except TestException:  # [catching-non-exception,try-except-raise]
        raise
    except Exception:
        pass

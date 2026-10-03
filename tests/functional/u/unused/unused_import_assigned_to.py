# pylint: disable=missing-docstring, import-error, invalid-name
# pylint: disable=too-few-public-methods, disallowed-name, no-member

import uuid

# Note this import doesn't actually exist
import foo

from .a import x


class Y:
    x = x[0]


def test(default=None):
    return default


class BaseModel:
    uuid = test(default=uuid.uuid4)


class bar:
    foo = foo.baz

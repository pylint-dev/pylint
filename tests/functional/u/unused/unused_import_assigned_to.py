# pylint: disable=missing-docstring, import-error, invalid-name
# pylint: disable=too-few-public-methods, blacklisted-name, no-member, useless-object-inheritance

import uuid

# Note this import doesn't actually exist
import foo

from .a import x


class Y(object):
    x = x[0]


def test(default=None):
    return default


class BaseModel(object):
    uuid = test(default=uuid.uuid4)


class bar(object):
    foo = foo.baz

# pylint: disable=missing-docstring, import-error, invalid-name
# pylint: disable=too-few-public-methods
from .a import x


class Y(object):
    x = x[0] # [redefined-outer-name]

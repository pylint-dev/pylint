"""collections.abc.Buffer is not counted as an ancestor either.

Split out from ``too_many_ancestors_abc`` because ``Buffer`` is only available
from Python 3.12 onwards.
"""
# pylint: disable=missing-class-docstring, too-few-public-methods, arguments-differ
from collections.abc import Buffer


class FromBuffer(Buffer):
    def __buffer__(self, flags):
        raise NotImplementedError

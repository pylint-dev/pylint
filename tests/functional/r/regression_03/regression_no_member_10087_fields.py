"""Imported by regression_no_member_10087.py.

Declares ``Field`` like ``pydantic`` does: ``@overload`` stubs whose body is only
``...``, then the implementation.
"""

# pylint: disable=invalid-name,unused-argument,too-few-public-methods

from typing import Any, Callable, overload


class FieldInfo:
    """What the implementation returns."""


@overload
def Field(default: Any) -> Any: ...
@overload
def Field(*, default_factory: Callable[[], Any]) -> Any: ...
def Field(default=None, *, default_factory=None):
    """Return the description of a field."""
    return FieldInfo()

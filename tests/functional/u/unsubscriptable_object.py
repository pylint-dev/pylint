"""Tests for unscubscriptable-object"""

# Test for typing.NamedTuple
# See: https://github.com/pylint-dev/pylint/issues/1295
import typing

MyType = typing.Tuple[str, str]

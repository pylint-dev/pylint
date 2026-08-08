"""Regression test for https://github.com/pylint-dev/pylint/issues/11229."""

from enum import Enum

# pylint: disable=invalid-name

enum_instance = Enum(1, "")
_ = enum_instance.missing  # [no-member]

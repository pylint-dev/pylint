"""Regression test from https://github.com/pylint-dev/pylint/issues/11229

The following code should not crash pylint, even though astroid infers
an integer as the Enum class name.
"""
# pylint: disable=too-few-public-methods

from enum import Enum

enum_instance = Enum(1, "")  # [invalid-name]
enum_instance.b  # [no-member, pointless-statement]  # noqa: B018

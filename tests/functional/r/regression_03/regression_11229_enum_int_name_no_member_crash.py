"""Regression test for https://github.com/pylint-dev/pylint/issues/11229.

``Enum(1, "")`` (functional API with a non-string class name) is invalid at
runtime, but astroid infers it as an instance whose ``name`` is the int ``1``.
The types checker must not crash in ``_emit_no_member`` when the owner name is
not a string; it should emit the regular ``no-member`` message instead of
raising ``TypeError`` (which turned into a fatal ``astroid-error``).
"""
# pylint: disable=missing-docstring, invalid-name
from enum import Enum

a = Enum(1, "")
print(a.b)  # [no-member]

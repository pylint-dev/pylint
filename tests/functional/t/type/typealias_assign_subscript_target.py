"""Regression test for a crash in the name checker when a chained assignment
of a ``TypeAlias`` value has a non-name target such as a ``Subscript``.

For ``a[0] = b = TypeAlias`` the first target of the ``Assign`` is a
``Subscript`` rather than an ``AssignName``; accessing ``.name`` on it
crashed with an ``AttributeError``.

https://github.com/pylint-dev/pylint/issues/11056
"""
# pylint: disable=invalid-name,undefined-variable

from typing import TypeAlias

a[0] = b = TypeAlias

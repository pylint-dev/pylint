# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/11053

Attribute access on a PEP 695 type parameter crashed ``visit_attribute``
because the ``TypeVar`` astroid node has no ``pytype()`` method.
"""

# pylint: disable=missing-docstring,pointless-statement


def f[T]():
    T.a

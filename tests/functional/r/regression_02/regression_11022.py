"""Regression test for https://github.com/pylint-dev/pylint/issues/11022.

Passing a non-constant value as the ``covariant`` or ``contravariant``
argument of ``TypeVar`` crashed the name checker, which assumed the
keyword value was always a constant.
"""

from typing import TypeVar

VARIANCE = True

T = TypeVar("T", covariant=VARIANCE)
T = TypeVar("T", contravariant=VARIANCE)

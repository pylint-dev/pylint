# pylint: disable=invalid-name,too-few-public-methods,unused-import,unused-variable
# pylint: disable=wrong-import-order,wrong-import-position
"""Functional tests for misplaced-module-dunder."""

from __future__ import annotations

__version__ = "1.0"
__author__: str = "Pylint contributors"

import os
from importlib import metadata
from typing import Final

__copyright__ = "2026"  # [misplaced-module-dunder]
__credits__: tuple[str, ...] = ()  # [misplaced-module-dunder]
__metadata_version__ = metadata.version("pylint")
__typed_version__: Final[str] = "1.0"
not_a_dunder = "allowed"
__ = "not a dunder name"


def function() -> None:
    """Nested dunders are outside the scope of this check."""
    __nested__ = "allowed"


class Klass:
    """Class dunders are outside the scope of this check."""

    __nested__ = "allowed"

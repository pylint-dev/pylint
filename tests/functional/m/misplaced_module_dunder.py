"""Module level dunder names should be placed before the imports (PEP 8)."""

from __future__ import annotations

__author__ = "Someone"
__copyright__: str = "Someone"
__credits__: list[str]

import os
import sys as system
from collections import OrderedDict

__version__ = "1.0.0"  # [misplaced-module-dunder]
__all__: list[str] = ["OrderedDict", "walk"]  # [misplaced-module-dunder]
__license__ = __maintainer__ = "MIT"  # [misplaced-module-dunder, misplaced-module-dunder]
__email__ = "a@b.c".upper()  # [misplaced-module-dunder]

# A value that refers to a name may depend on the imports above it
__status__ = os.environ.get("STATUS", "Production")
__contact__: str = system.prefix
__annotations__ = {name: str for name in ("a", "b")}
__contributors__: list[str]

# Only assignments to dunder names are concerned
NOT_A_DUNDER = "value"
NOT_A_DUNDER_EITHER: str = "value"
__all__ += ["system"]
__all__, _private = [], []

if system.version_info >= (3, 14):
    __doc__ = "Not at the module level"


def walk() -> None:
    """A function placed between the imports and a dunder."""
    __local__: str = "Not at the module level"
    print(__local__)


walk.__doc__: str = "Not a name"


__date__ = "2026-10-22"  # [misplaced-module-dunder]

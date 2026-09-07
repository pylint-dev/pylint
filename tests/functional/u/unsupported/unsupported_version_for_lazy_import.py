"""Test that PEP 810 lazy imports are reported when py-version is lower than 3.15."""
# pylint: disable=unused-import
lazy import statistics  # [using-lazy-import-in-unsupported-version]
lazy from pathlib import Path  # [using-lazy-import-in-unsupported-version]

# An eager import is fine on every version.
import math
from decimal import Decimal

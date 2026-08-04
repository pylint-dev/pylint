"""Tests for wrong-import-position with PEP 810 lazy imports."""
# pylint: disable=unused-import
CONST = 1

lazy import json  # [wrong-import-position]

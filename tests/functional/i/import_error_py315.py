"""Tests for import-error with PEP 810 lazy imports."""
# pylint: disable=unused-import
lazy import totally_missing_module_xyz  # [import-error]
lazy from another_missing_module_xyz import something  # [import-error]

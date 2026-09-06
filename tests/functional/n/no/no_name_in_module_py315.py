"""Tests for no-name-in-module with PEP 810 lazy imports."""
# pylint: disable=unused-import
lazy from collections import does_not_exist  # [no-name-in-module]

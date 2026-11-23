"""Tests for ungrouped-imports with PEP 810 lazy imports."""
# pylint: disable=unused-import
lazy from os import path
lazy import sys
lazy from os import walk  # [ungrouped-imports]

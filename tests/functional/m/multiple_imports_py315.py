"""Tests for multiple-imports with PEP 810 lazy imports."""
# pylint: disable=unused-import
lazy import os, sys  # [multiple-imports]
lazy import collections

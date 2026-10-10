"""Tests for wrong-import-order with PEP 810 lazy imports."""
# pylint: disable=unused-import
import astroid
lazy import os  # [wrong-import-order]

"""Tests for import aliasing messages with PEP 810 lazy imports."""
# pylint: disable=unused-import
lazy import collections.abc as abc  # [consider-using-from-import]
lazy import json as json  # [useless-import-alias]
lazy from os import path as path  # [useless-import-alias]
lazy from os import getcwd as cwd

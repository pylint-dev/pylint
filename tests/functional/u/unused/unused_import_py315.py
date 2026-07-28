"""Tests for unused-import with PEP 810 lazy imports."""
lazy import collections  # [unused-import]
lazy from json import dumps  # [unused-import]
lazy import os

print(os.getcwd())

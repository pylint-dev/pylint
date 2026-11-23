"""Tests for reimported with PEP 810 lazy imports."""
# pylint: disable=unused-import
import os
lazy import os  # [reimported]
lazy import sys
lazy import sys  # [reimported]
lazy import collections
import collections  # [reimported]

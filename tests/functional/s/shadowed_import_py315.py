"""Tests for shadowed-import with PEP 810 lazy imports."""
# pylint: disable=unused-import
import json
lazy from os import path as json  # [shadowed-import]

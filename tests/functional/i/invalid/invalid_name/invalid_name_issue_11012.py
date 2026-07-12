"""Tests for issue #11012: C0103 false positive for all-caps names at module level"""
# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods

import os
import sys

# All-caps names at module level assigned from function calls should be
# recognized as constants, not flagged as variables. (Issue #11012)

VERSION = os.path.basename
PYTHON = sys.version
MAINTAINER: str = os.path.basename

# Other test cases that should not be impacted
from collections import namedtuple
Class = namedtuple("a", ("b", "c"))

def A():
    return 1, 2, 3

CONSTD = A()
CONST = "12 34 ".rstrip().split()

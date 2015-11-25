"""Checks import order rule"""
# pylint: disable=unused-import,relative-import,ungrouped-imports,wrong-import-order,using-constant-test
# pylint: disable=import-error
import os.path
if True:
    from astroid import are_exclusive
try:
    import sys
except ImportError:
    import datetime

CONSTANT = True

import datetime  # [wrong-import-position]

VAR = 0
for i in range(10):
    VAR += i

import scipy  # [wrong-import-position]
import astroid  # [wrong-import-position]

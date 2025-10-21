"""Test wrong-import-position pragma scoping."""
# pylint: disable=unused-import

import os
import sys

# Pragma on non-import suppresses following imports until next non-import
CONSTANT_A = False  # pylint: disable=wrong-import-position
import time

CONSTANT_B = True
import logging  # [wrong-import-position]

# Inline pragma on import line
CONSTANT_C = 42
import json  # pylint: disable=wrong-import-position

"""Test wrong-import-position pragma on non-import statement."""
# pylint: disable=unused-import

import os
import sys

CONSTANT_A = False  # pylint: disable=wrong-import-position
import time

CONSTANT_B = True
import logging  # [wrong-import-position]

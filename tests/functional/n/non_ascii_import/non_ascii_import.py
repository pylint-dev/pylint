"""Test that invalid module name imports causes correct error"""
# pylint: disable=import-error, wrong-import-position, unused-wildcard-import, wildcard-import, wrong-import-order
import sys
import os

# allow module imports to test that this is indeed a valid python file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import non_ascii_name_loł as ok
from pathlib import *   # test that star imports work correctly and give no error

print(ok)

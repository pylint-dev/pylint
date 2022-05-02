"""Test that invalid module name do not cause errors when using an alias"""
# pylint: disable=import-error, wrong-import-position
import sys
import os

# allow module imports to test that this is indeed a valid python file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import non_ascii_name_loł as foobar

print(foobar)

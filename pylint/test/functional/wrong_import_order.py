"""Checks import order rule"""
# pylint: disable=unused-import,relative-import,ungrouped-imports

import six
import os.path  # [wrong-import-order]
from astroid import are_exclusive
import sys  # [wrong-import-order]
import datetime  # [wrong-import-order]
import unused_import
import scipy  # [wrong-import-order]
import astroid

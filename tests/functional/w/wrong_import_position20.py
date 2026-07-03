"""Checks wrong-import-position pragma scoping on non-import statements."""
# pylint: disable=unused-import

import os
import sys

CONSTANT_A = False  # pylint: disable=wrong-import-position
import time

CONSTANT_B = True
import logging  # [wrong-import-position]

CONSTANT_C = 42
import json  # pylint: disable=wrong-import-position

CONSTANT_D = "test"  # pylint: disable=wrong-import-position
import csv

CONSTANT_E = 123
import re  # [wrong-import-position]

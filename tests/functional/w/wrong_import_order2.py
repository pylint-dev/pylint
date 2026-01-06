"""Checks import order rule in a right case"""
# pylint: disable=unused-import,ungrouped-imports,import-error,no-name-in-module


# Standard imports
import os
from sys import argv

# external/third-party imports
import isort
import datetime  # std import that should be treated as third-party

# First-party imports
from six import moves

import pylint
import re  # std import that should be treated as first-party

# local_imports
from . import my_package
from .my_package import myClass

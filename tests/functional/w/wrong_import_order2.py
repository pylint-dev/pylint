"""Checks import order rule in a right case"""
# pylint: disable=unused-import,ungrouped-imports,import-error,no-name-in-module


# Standard imports
import os
from sys import argv

# external imports
import isort
import datetime  # std import that should be treated as third-party

from six import moves

# local_imports
from . import my_package
from .my_package import myClass

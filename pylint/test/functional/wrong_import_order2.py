"""Checks import order rule in a right case"""
# pylint: disable=unused-import,relative-import,ungrouped-imports,import-error,no-name-in-module


# Standard imports
import os
from sys import argv

# external imports
import isort

from six import moves

# local_imports
from . import my_package
from .my_package import myClass

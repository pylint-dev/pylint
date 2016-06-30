"""Checks import position rule"""
# pylint: disable=unused-import,relative-import,ungrouped-imports,import-error,no-name-in-module
A = 1
from sys import x  # [wrong-import-position]

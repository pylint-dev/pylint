"""Checks import position rule"""
# pylint: disable=unused-import,no-name-in-module
_ = 1
from sys import x  # [wrong-import-position]

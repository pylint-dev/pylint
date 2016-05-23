"""Checks import position rule"""
# pylint: disable=unused-import,relative-import,ungrouped-imports,wrong-import-order,using-constant-test
# pylint: disable=import-error, too-few-public-methods,missing-docstring

import os

try:
    import ast
except ImportError:
    def method(items):
        """docstring"""
        value = 0
        for item in items:
            value += item
        return value

import sys

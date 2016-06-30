"""Checks import position rule"""
# pylint: disable=unused-import,relative-import,ungrouped-imports,import-error,no-name-in-module,undefined-variable
if x:
    import os
import y  # [wrong-import-position]

"""Checks import position rule"""
# pylint: disable=unused-import,relative-import,ungrouped-imports,import-error,no-name-in-module
import y
try:
    import x
except ImportError:
    pass
else:
    pass

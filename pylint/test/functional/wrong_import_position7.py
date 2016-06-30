"""Checks import position rule"""
# pylint: disable=unused-import,relative-import,ungrouped-imports,import-error,no-name-in-module
try:
    import x
except ImportError:
    pass
finally:
    pass
import y

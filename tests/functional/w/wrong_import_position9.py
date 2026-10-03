"""Checks import position rule"""
# pylint: disable=unused-import,ungrouped-imports,import-error,no-name-in-module,relative-beyond-top-level
import y
try:
    import x
except ImportError:
    pass
else:
    pass

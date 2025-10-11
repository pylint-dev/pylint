"""Checks that disabling 'wrong-import-position' only affects the specific line.

A pragma on a non-import statement should not affect subsequent import statements.
This demonstrates the correct behavior after fixing the bug.
"""
# pylint: disable=unused-import

CONSTANT = True  # pylint: disable=wrong-import-position

import sys  # [wrong-import-position]

"""Checks that disabling 'wrong-import-position' on a statement prevents it from
invalidating subsequent imports."""
# pylint: disable=unused-import

CONSTANT = True  # pylint: disable=wrong-import-position

import sys

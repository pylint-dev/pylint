"""test module importing itself"""
# pylint: disable=no-absolute-import,using-constant-test
from __future__ import print_function
from . import import_itself  # [import-self]

__revision__ = 0


if __revision__:
    print(import_itself)

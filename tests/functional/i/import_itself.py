"""test module importing itself"""
# pylint: disable=using-constant-test
from . import import_itself  # [import-self]

__revision__ = 0


if __revision__:
    print(import_itself)

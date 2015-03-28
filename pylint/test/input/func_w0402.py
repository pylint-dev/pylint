"""test wildard import
"""
__revision__ = 0
# pylint: disable=no-absolute-import
from input.indirect1 import *
# This is an unresolved import which still generates the wildcard-import
# warning.
from unknown.package import *

def abcd():
    """use imports"""
    TotoInterface()

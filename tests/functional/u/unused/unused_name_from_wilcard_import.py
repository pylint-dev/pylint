"""check unused import from a wildcard import"""
# pylint: disable=no-absolute-import,line-too-long
from .unused_argument_py3 import *  # [unused-wildcard-import, unused-wildcard-import, wildcard-import]

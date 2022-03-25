"""check unused import from a wildcard import"""
# pylint: disable=line-too-long
from .unused_argument_py3 import *  # [unused-wildcard-import, wildcard-import]
from .unused_global_variable1 import * # [unused-wildcard-import, wildcard-import]
from .unused_import_py30 import * # [unused-wildcard-import, wildcard-import]

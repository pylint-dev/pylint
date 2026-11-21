"""Check that a wildcard import only reports the names its module exports."""

from .unused_wildcard_import_all_helper import *  # [unused-wildcard-import, wildcard-import]

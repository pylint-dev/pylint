"""Check that ``from . import *`` only reports the names the package exports."""

from . import *  # [unused-wildcard-import, wildcard-import]

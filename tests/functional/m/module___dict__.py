"""https://www.logilab.org/ticket/6949."""
from __future__ import print_function
__revision__ = None

print(__dict__ is not None)  # [used-before-assignment]

__dict__ = {}

print(__dict__ is not None)

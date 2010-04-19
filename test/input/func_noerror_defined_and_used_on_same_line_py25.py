# pylint: disable=C0321
"""test http://www.logilab.org/ticket/6954"""

from __future__ import with_statement

__revision__ = None

with file('f') as f: print f.read()

"""test relative import
"""
__revision__ = apply(map, (str, (1, 2, 3)))
from __future__ import generators

import func_w0302

def function():
    """something"""
    print func_w0302
    unic = u"unicode"
    low = unic.looower
    return low



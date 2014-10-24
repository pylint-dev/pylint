"""test relative import"""
# pylint: disable=no-absolute-import
__revision__ = filter(None, map(str, (1, 2, 3)))
from __future__ import generators, print_function

import func_w0302

def function():
    """something"""
    print(func_w0302)
    unic = u"unicode"
    low = unic.looower
    return low

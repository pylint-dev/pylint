"""test relative import"""
# pylint: disable=no-absolute-import
from __future__ import print_function
__revision__ = filter(None, map(str, (1, 2, 3)))

import func_w0302

def function():
    """something"""
    print(func_w0302)
    unic = u"unicode"
    low = unic.looower
    return low

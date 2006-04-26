"""check reimport
"""

__revision__ = 0

import os
from os.path import join, exists

import os
import re as _re

_re.match('yo', '.*')

if __revision__:
    print os
    from os.path import exists
    print join, exists

def func(yooo):
    """reimport in different scope"""
    import os as ass
    ass.remove(yooo)
    import re
    re.compile('.*')
    
if 1:
    import sys
    print sys.modules
else:
    print 'bla'
    import sys

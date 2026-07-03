"""check reimport
"""

# pylint: disable=using-constant-test,ungrouped-imports,wrong-import-position,import-outside-toplevel
import os
from os.path import join, exists
import os  # [reimported]
import re as _re

__revision__ = 0
_re.match('yo', '.*')

if __revision__:
    print(os)
    from os.path import exists  # [reimported]
    print(join, exists)

def func(yooo):
    """reimport in different scope"""
    import os as ass  # [reimported]
    ass.remove(yooo)
    import re  # [reimported]
    re.compile('.*')

if 1: # pylint: disable=using-constant-test
    import sys
    print(sys.modules)
else:
    print('bla')
    import sys

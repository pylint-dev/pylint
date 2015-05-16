#pylint: disable=W0401,W0611,no-absolute-import,invalid-name,import-error
"""check unexistant names imported are reported"""
from __future__ import print_function

import logilab.common.tutu  # [no-name-in-module]
from logilab.common import toto  # [no-name-in-module]
toto.yo()

from logilab.common import modutils
modutils.nonexistant_function()  # [no-member]
modutils.another.nonexistant.function()  # [no-member]
print(logilab.common.modutils.yo)  # [no-member]

import sys
print(sys.stdout, 'hello world')
print(sys.stdoout, 'bye bye world')  # [no-member]


import re
re.finditer('*', 'yo')

from rie import *
from re import findiiter, compiile  # [no-name-in-module,no-name-in-module]

import os
'SOMEVAR' in os.environ  # [pointless-statement]

try:
    from collections import something
except ImportError:
    something = None

try:
    from collections import anything # [no-name-in-module]
except ValueError:
    anything = None

try:
    import collections.missing
except ImportError:
    pass

try:
    import collections.indeed_missing # [no-name-in-module]
except ValueError:
    pass

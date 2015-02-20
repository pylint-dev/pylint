#pylint: disable=W0401,W0611,print-statement,no-absolute-import
"""check unexistant names imported are reported"""


import logilab.common.tutu  # [no-name-in-module,import-error]
from logilab.common import toto  # [no-name-in-module]
toto.yo()

from logilab.common import modutils
modutils.nonexistant_function()  # [no-member]
modutils.another.nonexistant.function()  # [no-member]
print logilab.common.modutils.yo  # [no-member]

import sys
print >> sys.stdout, 'hello world'
print >> sys.stdoout, 'bye bye world'  # [no-member]


import re
re.finditer('*', 'yo')

from rie import *  # [import-error]
from re import findiiter, compiile  # [no-name-in-module,no-name-in-module]

import os
'SOMEVAR' in os.environ  # [pointless-statement]

# pylint: disable=wildcard-import,unused-import,invalid-name,import-error
# pylint: disable=bare-except,broad-except,wrong-import-order,ungrouped-imports,wrong-import-position
"""check nonexistent names imported are reported"""

import collections.tutu  # [no-name-in-module]
from collections import toto  # [no-name-in-module]
toto.yo()

from xml.etree import ElementTree
ElementTree.nonexistent_function()  # [no-member]
ElementTree.another.nonexistent.function()  # [no-member]


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
    import collections.missing
except ModuleNotFoundError:
    pass

try:
    import collections.indeed_missing # [no-name-in-module]
except ValueError:
    pass

try:
    import collections.emit # [no-name-in-module]
except Exception:
    pass

try:
    import collections.emit1
except ImportError:
    pass

try:
    import collections.emit1
except ModuleNotFoundError:
    pass


try:
    if something:
        import collections.emit2 # [no-name-in-module]
except Exception:
    pass

from .no_self_argument import NoSelfArgument
from .no_self_argument import lala  # [no-name-in-module]
from .no_self_argument.bla import lala1 # [no-name-in-module]

# Check ignored-modules setting
from argparse import THIS_does_not_EXIST


# This captures the original failure in https://github.com/pylint-dev/pylint/issues/6497
# only if numpy is installed. We are not installing numpy on CI (for now)
from numpy.distutils.misc_util import is_sequence
from pydantic import BaseModel

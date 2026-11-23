"""Test deprecated imports inside version and non-version guards."""
# pylint: disable=no-name-in-module,unused-import

import sys

if sys.version_info >= (3, 9):
    from collections.abc import Set
else:
    from collections import Set

if sys.platform == "win32":
    from collections import Iterable  # [deprecated-class]

if sys.version_info >= (3, 3):
    from xml.etree.cElementTree import Element  # [deprecated-module]

# The guard counts however `sys.version_info` is spelled
from sys import version_info

if version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from collections import Mapping

if (3, 9) <= version_info:
    from collections.abc import Sequence
else:
    from collections import Sequence

if version_info[:2] >= (3, 9):
    from collections.abc import Sized
else:
    from collections import Sized

# A name that merely looks like the version does not guard anything
from collections import OrderedDict as version_info_fake

if version_info_fake >= (3, 9):
    from collections import Callable  # [deprecated-class]

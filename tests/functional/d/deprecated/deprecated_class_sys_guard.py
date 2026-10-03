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

"""Do not emit deprecated-class for imports protected by a version guard."""
# pylint: disable=unused-import

import sys

if sys.version_info >= (3, 9):
    from collections.abc import Set
else:
    from collections import Set

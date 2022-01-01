# pylint: disable=unused-import, missing-docstring, reimported, import-error, wrong-import-order, no-name-in-module, multiple-imports, ungrouped-imports, misplaced-future

from _world import hello # [import-private-name]
from _world import _hello # [import-private-name]
from city import _house # [import-private-name]
from city import a, _b, c, _d # [import-private-name]
from _city import a, _b, c, _d # [import-private-name]
from city import a, b, c, _d # [import-private-name]
import house
import _house # [import-private-name]
import _house, _chair, _stair # [import-private-name]
import house, _chair, _stair # [import-private-name]

# Ignore dunders
import __asd__
import __future__
from __future__ import print_function
from __future__ import __print_function__

# Ignore local modules
from pylint import _private
from pylint.checkers import _private
from . import _private
from astroid import _private # [import-private-name]
from sys import _private # [import-private-name]

# Ignore typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import _TreeType
    from types import _TreeType
    from _types import TreeType
    from _types import _TreeType

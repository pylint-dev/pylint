# pylint: disable=unused-import, missing-docstring, reimported, import-error, wrong-import-order, no-name-in-module, multiple-imports, ungrouped-imports, misplaced-future, wrong-import-position

from _world import hello  # [import-private-name]
from _world import _hello  # [import-private-name]
from city import _house  # [import-private-name]
from city import a, _b, c, _d  # [import-private-name]
from _city import a, _b, c, _d  # [import-private-name]
from city import a, b, c, _d  # [import-private-name]
import house
import _house  # [import-private-name]
import _house, _chair, _stair  # [import-private-name]
import house, _chair, _stair  # [import-private-name]

# Ignore dunders
import __asd__
import __future__
from __future__ import print_function
from __future__ import __print_function__

# Ignore local modules
# The check for local modules compares directory names in the path of the file being linted to
# the name of the module we are importing from. The use of `__init__.py` to indicate Python modules
# is deprecated so this is a heuristic solution.
# If we were importing from `pylint`, it would be counted as a valid internal private import
# and not emit a message as long as this file has a parent directory called `pylint`, even though
# we are not importing from that directory. (We would be importing from `pylint/pylint`.)
from private_import import _private  # pylint: disable=import-self
from private_import.other_file import _private
from . import _private
from astroid import _private  # [import-private-name]
from sys import _private  # [import-private-name]

# Ignore typecheck
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    import _TreeType
    from types import _TreeType
    from _types import TreeType
    from _types import _TreeType

# No error since imports are used as typing
from classes import _PrivateClassA
from classes import _PrivateClassB
from classes import _PrivateClassC

a: _PrivateClassA


def b_func(class_b: _PrivateClassB):
    print(class_b)


def c_func() -> _PrivateClassC:
    return None


from classes import _SubScriptA
from classes import _SubScriptB

a: Optional[_SubScriptA]
b: Optional[_SubScriptB[List]]

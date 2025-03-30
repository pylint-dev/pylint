"""Tests for import-private-name."""
# pylint: disable=unused-import, missing-docstring, reimported, import-error, wrong-import-order
# pylint: disable=no-name-in-module, multiple-imports, ungrouped-imports, misplaced-future
# pylint: disable=wrong-import-position, relative-beyond-top-level

# Basic cases
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

# No error since imports are used as type annotations
from classes import _PrivateClassA, safe_get_A
from classes import _PrivateClassB
from classes import _PrivateClassC

a_var: _PrivateClassA = safe_get_A()

def b_func(class_b: _PrivateClassB):
    print(class_b)

def c_func() -> _PrivateClassC:
    return None

# Used as typing in slices
from classes import _SubScriptA
from classes import _SubScriptB

a: Optional[_SubScriptA]
b: Optional[_SubScriptB[List]]

import _TypeContainerA
import _TypeContainerB
import _TypeContainerC

import SafeContainerA
a2: _TypeContainerA.A = SafeContainerA.safe_get_a()

def b_func2(class_b2: _TypeContainerB.B):
    print(class_b2)

def c2_func() -> _TypeContainerC.C:
    return None

# This is allowed since all the imports are used for typing
from _TypeContainerExtra import TypeExtraA, TypeExtraB
from MakerContainerExtra import GetA, GetB
extra_a: TypeExtraA = GetA()
extra_b: TypeExtraB = GetB()

# This is not allowed because there is an import not used for typing
from _TypeContainerExtra2 import TypeExtra2, NotTypeExtra # [import-private-name]
extra2: TypeExtra2

# Try many cases to ensure that type annotation usages of a private import
# do not mask other illegal usages of the import
import _private_module # [import-private-name]
my_var: _private_module.Thing = _private_module.Thing()

import _private_module2 # [import-private-name]
my_var2: _private_module2.Thing2
my_var2 = _private_module2.Thing2()

import _private_module3 # [import-private-name]
my_var3: _private_module3.Thing3
my_var3 = _private_module3.Thing3
my_var3_2: _private_module3.Thing3

import _private_module4 # [import-private-name]
my_var4: _private_module4.Thing4
my_var4 = _private_module4.get_callers().get_thing4()

from _private_module5 import PrivateClass # [import-private-name]
my_var5: PrivateClass
my_var5 = PrivateClass()

from _private_module6 import PrivateClass2 # [import-private-name]
my_var6: PrivateClass2 = PrivateClass2()

from public_module import _PrivateClass3 # [import-private-name]
my_var7: _PrivateClass3 = _PrivateClass3()

# Even though we do not see the private call, the type check does not keep us from emitting
# because we do not use that variable
import _private_module_unreachable # [import-private-name]
my_var8: _private_module_unreachable.Thing8
_private_module_unreachable.Thing8()


# pylint: disable=too-few-public-methods
class Regression6624:
    """Ensure that an import statement precedes this case."""
    def get_example(self):
        example: Example = Example().save()
        return example


class Example:
    def save(self):
        return self


# Treat relative imports as internal
from .other_file import _private
from ..parent import _private

from _private_module_x import some_name # [import-private-name]
VAR = some_name

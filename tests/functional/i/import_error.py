""" Test that import errors are detected. """
# pylint: disable=invalid-name, unused-import, bare-except, broad-except, wrong-import-order, wrong-import-position
import totally_missing # [import-error]

try:
    import maybe_missing
except ImportError:
    maybe_missing = None

try:
    import maybe_missing
except ModuleNotFoundError:
    maybe_missing = None

try:
    import maybe_missing_1
except (ImportError, SyntaxError):
    maybe_missing_1 = None

try:
    import maybe_missing_2 # [import-error]
except ValueError:
    maybe_missing_2 = None


try:
    if maybe_missing:
        import really_missing
except ImportError:
    pass


from functional.s.syntax_error import toto  # [no-name-in-module,syntax-error]


# Don't emit `import-error` or `no-name-in-module`
# if guarded behind `sys.version_info` or `typing.TYPE_CHECKING`
import sys
import typing
import typing as tp  # pylint: disable=reimported
from typing import TYPE_CHECKING


if sys.version_info >= (3, 9):
    import some_module
    from some_module import some_class
else:
    import some_module_alt

if sys.version_info[:2] >= (3, 9):
    import some_module
else:
    import some_module_alt


if typing.TYPE_CHECKING:
    import stub_import

if tp.TYPE_CHECKING:
    import stub_import

if TYPE_CHECKING:
    import stub_import
    from stub_import import stub_class


# Test ignore-modules option
from external_module import anything

from external_module.another_module import anything

import external_module

from fake_module.submodule import anything

from fake_module.submodule.deeper import anything

import foo, bar # [multiple-imports]

import foo
import bar

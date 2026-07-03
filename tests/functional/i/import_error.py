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


from functional.s.syntax.syntax_error import toto  # [no-name-in-module,syntax-error]


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

import mymodule_ignored
import mymodule.something_ignored
from mymodule.something_ignored import anything
import sys.something_ignored
from sys.something_ignored import anything

# Issues with contextlib.suppress reported in
# https://github.com/pylint-dev/pylint/issues/7270
import contextlib
with contextlib.suppress(ImportError):
    import foo2

with contextlib.suppress(ValueError):
    import foo2  # [import-error]

with contextlib.suppress(ImportError, ValueError):
    import foo2

with contextlib.suppress((ImportError, ValueError)):
    import foo2

with contextlib.suppress((ImportError,), (ValueError,)):
    import foo2

x = True
with contextlib.suppress(ImportError):
    if x:
        import foo2
    else:
        pass

with contextlib.suppress(ImportError):
    with contextlib.suppress(TypeError):
        import foo2

""" Test that import errors are detected. """
# pylint: disable=invalid-name, unused-import, no-absolute-import, bare-except, broad-except, wrong-import-order, wrong-import-position
import totally_missing # [import-error]

try:
    import maybe_missing
except ImportError:
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
    import zoneinfo
    from zoneinfo import zone_class
else:
    import zoneinfo_alt

if sys.version_info[:2] >= (3, 9):
    import zoneinfo
else:
    import zoneinfo_alt


if typing.TYPE_CHECKING:
    import stub_import

if tp.TYPE_CHECKING:
    import stub_import

if TYPE_CHECKING:
    import stub_import
    from stub_import import stub_class

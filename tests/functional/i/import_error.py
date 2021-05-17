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

# pylint: disable=no-name-in-module
from functional.s.syntax_error import toto # [syntax-error]

# Don't emit import-error if guarded behind `sys.version_info`
import sys

if sys.version_info >= (3, 9):
    import zoneinfo

if sys.version_info[:2] >= (3, 9):
    import zoneinfo

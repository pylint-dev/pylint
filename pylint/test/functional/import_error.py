""" Test that import errors are detected. """
# pylint: disable=invalid-name, unused-import, no-absolute-import
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

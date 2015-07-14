""" Test that import errors are detected. """
# pylint: disable=invalid-name, unused-import, no-absolute-import, bare-except, broad-except
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
    import dont_emit
except Exception:
    pass

try:
    import please_dont_emit
except:
    pass

try:
    if maybe_missing:
        import really_missing
except ImportError:
    pass

from .collections import missing # [import-error]

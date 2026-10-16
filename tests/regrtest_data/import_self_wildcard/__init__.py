"""Package whose __init__.py imports itself via ``from ... import *``.

Regression fixture for issue #3748: a self-referential wildcard import is a
genuine self-import and must still be reported after the fix for the
missing-name false positive.
"""
from import_self_wildcard import *  # noqa: F401,F403

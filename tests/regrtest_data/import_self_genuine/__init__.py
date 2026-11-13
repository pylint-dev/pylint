"""Package whose __init__.py imports itself via a plain ``import`` statement.

Regression fixture for issue #3748: a plain self-import is a genuine
import-self and must still be reported after the fix for the false positive
on a name that does not exist anywhere in the package.
"""
import import_self_genuine

print(import_self_genuine)

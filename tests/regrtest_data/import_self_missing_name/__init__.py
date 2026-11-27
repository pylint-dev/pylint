"""Package whose __init__.py imports a name that does not exist anywhere in
the package.

Regression fixture for issue #3748: this used to be misreported as
import-self, even though nothing here imports the package itself.
"""
from import_self_missing_name import totally_missing_name

print(totally_missing_name)

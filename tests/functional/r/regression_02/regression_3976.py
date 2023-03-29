"""
Regression test for https://github.com/pylint-dev/pylint/issues/3976

E1123: Unexpected keyword argument 'include_extras' in function call (unexpected-keyword-arg)
"""

import typing_extensions


def function():
    """Simple function"""


typing_extensions.get_type_hints(function, include_extras=True)

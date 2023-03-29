"""Regression test for issue 5770: NewType created with f-string
See: https://github.com/pylint-dev/pylint/issues/5770
"""
from typing import NewType

def make_new_type(suffix):
    """Dynamically create a NewType with `suffix`"""
    new_type = NewType(f'IntRange_{suffix}', suffix)
    print(new_type)

"""Test disabling of cyclic import check inside a function
"""
# pylint: disable=no-absolute-import
from __future__ import print_function


def func():
    """Test disabling of cyclic import check inside a function"""
    from . import w0401_cycle  # pylint: disable=cyclic-import
    if w0401_cycle:
        print(w0401_cycle)

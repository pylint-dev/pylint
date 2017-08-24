"""Unittests for W1125 (kw args before *args)"""
from __future__ import absolute_import, print_function

# pylint: disable=unused-argument
def check_kwargs_before_args(param1, param2=2, *args):
    """docstring"""
    pass

check_kwargs_before_args(5)

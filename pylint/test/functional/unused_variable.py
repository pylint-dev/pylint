# pylint: disable=missing-docstring, invalid-name

def test_regression_737():
    import xml # [unused-variable]

def test_regression_923():
    import unittest.case  # [unused-variable]
    import xml as sql # [unused-variable]

def test_unused_with_prepended_underscore():
    _foo = 42
    _ = 24
    __a = 24
    dummy = 24
    _a_ = 42 # [unused-variable]
    __a__ = 24 # [unused-variable]

# pylint: disable=missing-docstring,invalid-name

# Test that global variables matching dummy-variables-rgx are not
# reported as unused (issue #10890).

_ = []  # This should NOT trigger unused-variable
__ = {}  # This should NOT trigger unused-variable

var = "pylint"  # [unused-variable]

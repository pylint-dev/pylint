"""Regression test for issue 5461
Crash on list comprehension with it used `type` as variable name

See: https://github.com/pylint-dev/pylint/issues/5461
"""
VAR = [type for type in [] if type["id"]]

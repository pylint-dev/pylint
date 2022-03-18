"""Regression test for issue 5461
Crash on list comprehension with it used `type` as variable name

See: https://github.com/PyCQA/pylint/issues/5461
"""
var = [type for type in [] if type["id"]]

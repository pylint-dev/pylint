# pylint: disable=too-few-public-methods, missing-docstring
# pylint: disable=useless-object-inheritance
"""Class scope must be handled correctly in genexps"""
class MyClass(object):
    var1 = []
    var2 = list(value*2 for value in var1)

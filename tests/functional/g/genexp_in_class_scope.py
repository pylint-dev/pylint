# pylint: disable=too-few-public-methods, missing-docstring
"""Class scope must be handled correctly in genexps"""
class MyClass:
    var1 = []
    var2 = list(value*2 for value in var1)

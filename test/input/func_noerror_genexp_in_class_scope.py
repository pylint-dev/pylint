# pylint: disable=W0232,R0903
"""class scope must be handled correctly in genexps"""

__revision__ = ''

class MyClass:
    """ds"""
    var1 = []
    var2 = list(value*2 for value in var1)

# pylint: disable=R0903, useless-object-inheritance
"""#10075"""

__revision__ = 1

class Aaa(object):
    """docstring"""
    def __init__(self):
        def inner_function(arg):
            """inner docstring"""
            return arg + 4
        self.func = inner_function

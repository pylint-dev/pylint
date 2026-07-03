# pylint: disable=too-few-public-methods
"""#10075"""


class Aaa:
    """docstring"""
    def __init__(self):
        def inner_function(arg):
            """inner docstring"""
            return arg + 4
        self.func = inner_function

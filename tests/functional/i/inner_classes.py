# pylint: disable=too-few-public-methods, unnecessary-pass, unnecessary-dunder-call
"""Backend Base Classes for the schwelm user DB"""

__revision__ = "alpha"

class Aaa:
    """docstring"""
    def __init__(self):
        self.__setattr__('a', 'b')


    def one_public(self):
        """docstring"""
        pass

    def another_public(self):
        """docstring"""
        pass

class Bbb(Aaa):
    """docstring"""
    pass

class Ccc(Aaa):
    """docstring"""

    class Ddd(Aaa):
        """docstring"""
        pass

    class Eee(Ddd):
        """docstring"""
        pass

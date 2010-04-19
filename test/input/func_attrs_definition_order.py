# pylint: disable=R0903
"""yo"""

__revision__ = '$I$'

class Aaaa:
    """class with attributes defined in wrong order"""
    def __init__(self):
        var1 = self._var2
        self._var2 = 3
        print var1

class Bbbb(object):
    """hop"""
    __revision__ = __revision__ # no problemo marge
    
    def __getattr__(self, attr):
        # pylint: disable=W0201
        try:
            return self.__repo
        except AttributeError:
            self.__repo = attr
            return attr

    
    def catchme(self, attr):
        """no AttributeError catched"""
        # pylint: disable=W0201
        try:
            return self._repo
        except ValueError:
            self._repo = attr
            return attr

# pylint: disable=R0903, print-statement
"""crash test"""

__revision__ = 1

class Temelekefe(object):
    """gloubliboulga"""

    def __init__(self):
        """nested class with function raise error"""
        class Toto(object):
            """toto nested class"""
            def __init__(self):
                self.attr = 2
            def toto_method(self):
                """toto nested class method"""
                print self
        print 'error ?', self, Toto

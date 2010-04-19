# pylint: disable=R0903
"""crash test"""

__revision__ = 1

class Temelekefe:
    """gloubliboulga"""
    
    def __init__(self):
        """nested class with function raise error"""
        class Toto:
            """toto nested class"""
            def __init__(self):
                self.attr = 2
            def toto_method(self):
                """toto nested class method"""
                print self
        print 'error ?', self, Toto

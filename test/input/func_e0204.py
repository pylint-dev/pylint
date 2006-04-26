"""check for method without self as first argument
"""

__revision__ = 0


class Abcd:
    """dummy class"""

    def __init__(truc):
        """method without self"""
        print 1

    def abdc(yoo):
        """another test"""
        print yoo
    def edf(self):
        """just another method"""
        print 'yapudju in', self

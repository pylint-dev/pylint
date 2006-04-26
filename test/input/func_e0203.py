"""check for method without self as first argument
"""

__revision__ = 0


class Abcd:
    """dummy class"""
    def __init__(self):
        pass

    def abcd(yoo):
        """another test"""

    abcd = classmethod(abcd)

    def edf(self):
        """justo ne more method"""
        print 'yapudju in', self

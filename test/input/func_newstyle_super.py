# pylint: disable=R0903
"""check use of super"""
__revision__ = None

class Aaaa:
    """old style"""
    def hop(self):
        """hop"""
        super(Aaaa, self).hop()

    def __init__(self):
        super(Aaaa, self).__init__()

class NewAaaa(object):
    """old style"""
    def hop(self):
        """hop"""
        super(NewAaaa, self).hop()

    def __init__(self):
        super(object, self).__init__()
        

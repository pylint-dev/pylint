# pylint: disable=R0903,W0232
"""check for scope problems"""

__revision__ = None

class Well(object):
    """well"""
    class Data: 
        """base hidden class"""
    class Sub(Data):
        """whaou, is Data found???"""
        yo = Data()
    def func(self):
        """check Sub is not defined here"""
        return Sub(), self

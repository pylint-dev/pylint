"""check unused import
"""
__revision__ = 1
import os
import sys

class NonRegr:
    """???"""
    def __init__(self):
        print 'initialized'

    def sys(self):
        """should not get sys from there..."""
        print self, sys

    def dummy(self, truc):
        """yo"""
        return self, truc
    
    def blop(self):
        """yo"""
        print self, 'blip'

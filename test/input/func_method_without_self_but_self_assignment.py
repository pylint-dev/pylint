# pylint: disable=R0903
"""regression test: setup() leads to "unable to load module..."
"""

__revision__ = 1

class Example:
    """bla"""
    
    def __init__(self):
        pass

    def setup():
        "setup without self"
        self.foo = 1

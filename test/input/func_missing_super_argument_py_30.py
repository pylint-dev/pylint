"""Check missing super argument for Python 2"""

__revision__ = 0

class MyClass(object):
    """ New style class """
    def __init__(self):
        super().__init__()
		
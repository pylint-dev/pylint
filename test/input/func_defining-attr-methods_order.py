# pylint: disable=C0103

''' Test that y is defined properly, z is not.
    Default defining methods are __init__, 
    __new__, and setUp.
    Order of methods should not matter. '''

__revision__ = ''

class A:
    ''' class A '''

    def __init__(self):
        ''' __init__ docstring filler '''
        self.x = 0
        self.setUp()

    def set_y(self, y):
        ''' set_y docstring filler '''
        self.y = y

    def set_x(self, x):
        ''' set_x docstring filler '''
        self.x = x

    def set_z(self, z):
        ''' set_z docstring filler '''
        self.z = z

    def setUp(self):
        ''' setUp docstring filler '''
        self.x = 0
        self.y = 0

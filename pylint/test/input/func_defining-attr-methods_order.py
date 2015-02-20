# pylint: disable=C0103, too-few-public-methods

''' Test that y is defined properly, z is not.
    Default defining methods are __init__,
    __new__, and setUp.
    Order of methods should not matter. '''

__revision__ = ''

class A(object):
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
        self.z = z

    def setUp(self):
        ''' setUp docstring filler '''
        self.x = 0
        self.y = 0

class B(A):
    ''' class B '''

    def test(self):
        """ test """
        self.z = 44

class C(object):
    ''' class C '''

    def __init__(self):
        self._init()

    def _init(self):
        ''' called by __init__ '''
        self.z = 44

class D(object):
    ''' class D '''

    def setUp(self):
        ''' defining method '''
        self.set_z()

    def set_z(self):
        ''' called by the parent. '''
        self.z = 42

class E(object):
    ''' Reassign the function. '''

    def __init__(self):
        i = self._init
        i()

    def _init(self):
        ''' called by __init__ '''
        self.z = 44

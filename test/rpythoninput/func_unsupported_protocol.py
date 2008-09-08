# pylint: disable-msg=E1202
import os

class C(object):
    def __new__(cls, *args):
        os.write('new!')
        return object.__new__(cls, *args)
    
    def __init__(self, a):
        self.attr = a

    def __add__(self, other):
        return self.attr + other
    
def function(l):
    os.write(1, '%s\n' % (C(len(l)) + 4))

def entry_point(argv):
    function(argv)
    return 0

def target(*args):
    return entry_point, None

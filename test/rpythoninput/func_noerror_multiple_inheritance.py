class A:
    def __init__(self):
        self.parentattr = None

class B:
    _mixin_ = True

class C(A, B):
    def __init__(self, a):
        A.__init__(self, a)
        self.attr = a


def function(l):
    os.write(1, '%s\n' % C(l))

def entry_point(argv):
    function(argv)
    return 0

def target(*args):
    return entry_point, None

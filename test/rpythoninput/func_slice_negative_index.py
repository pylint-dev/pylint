import os

A = -1
B = -2

def function(l, step=1):
    os.write(1, '%s\n' % l[-1:])
    os.write(1, '%s\n' % l[1:-1])
    os.write(1, '%s\n' % l[A:B])
    os.write(1, '%s\n' % l[-1:B:A])
    os.write(1, '%s\n' % l[-1::])
    os.write(1, '%s\n' % l[::-1])


def entry_point(argv):
    function([1, 2, 3, 4, 5, 6])
    return 0

def target(*args):
    return entry_point, None

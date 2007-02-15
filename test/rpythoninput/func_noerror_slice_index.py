import os

def function(l):
    os.write(1, '%s\n' % l[:-1])
    os.write(1, '%s\n' % l[0:-1])
    os.write(1, '%s\n' % l[:-1:])
    os.write(1, '%s\n' % l[0:2])
    step = 1
    os.write(1, '%s\n' % l[0:2:step])


def entry_point(argv):
    function([1, 2, 3, 4, 5, 6])
    return 0

def target(*args):
    return entry_point, None

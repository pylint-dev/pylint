import os

def function(l, step=1):
    os.write(1, '%s\n' % l[1:3:step])


def entry_point(argv):
    function([1, 2, 3, 4, 5, 6], len(argv))
    return 0

def target(*args):
    return entry_point, None

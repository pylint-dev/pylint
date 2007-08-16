import os

def function(l):
    os.write(1, '%s\n' % ';'.join(str(v) for v in l))

def entry_point(argv):
    function([1, 2, 3, 4, 5, 6])
    return 0

def target(*args):
    return entry_point, None

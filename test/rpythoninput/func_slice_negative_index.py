A = -1
B = -2

def function(l):
    print l[-1:]
    print l[:-1]
    print l[A:B]
    print l[-1:B:A]
    print l[-1::]
    print l[:-1:]
    print l[::-1]


def entry_point(argv):
    function([1, 2, 3, 4, 5, 6])
    return 0

def target(*args):
    return entry_point, None

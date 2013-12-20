"""Check for else branches on loops with break an return only."""

__revision__ = 0

def test_return_for():
    """else + return is not accetable."""
    for i in range(10):
        if i % 2:
            return i
    else:
        print 'math is broken'

def test_return_while():
    """else + return is not accetable."""
    while True:
        return 1
    else:
        print 'math is broken'


while True:
    def short_fun():
        """A function with a loop."""
        for _ in range(10):
            break
else:
    print 'or else!'


while True:
    while False:
        break
else:
    print 'or else!'

for j in range(10):
    pass
else:
    print 'fat chance'
    for j in range(10):
        break

def test_return_for2():
    """no false positive for break in else

    https://bitbucket.org/logilab/pylint/issue/117/useless-else-on-loop-false-positives
    """
    for i in range(10):
        for i in range(i):
            if i % 2:
                break
        else:
            break
    else:
        print 'great math'

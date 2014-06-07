"""test for Python 3 string formatting error
"""

__revision__ = 1

def pprint():
    """Test string format """
    print "{} {".format()
    print "{} }".format()
    print "{0} {1}".format(1, 2)
    print "{0} {1} {a}".format(1, 2, 3)
    print "{a} {b}".format(a=1, c=2)
    print "{} {a}".format(1, 2)
    print "{} {}".format(1)
    print "{} {}".format(1, 2, 3)
    print "{a} {b} {c}".format()
    print "{} {}".format(a=1, b=2)
    print "{a} {b}".format(1, 2)

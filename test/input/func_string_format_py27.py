"""test for Python 3 string formatting error
"""
# pylint: disable=too-few-public-methods, import-error, unused-argument, star-args
import os
from missing import Missing

__revision__ = 1

class Custom(object):
    """ Has a __getattr__ """
    def __getattr__(self):
        return self

class Test(object):
    """ test format attribute access """
    custom = Custom()
    ids = [1, 2, 3, [4, 5, 6]]

class Getitem(object):
    """ test custom getitem for lookup access """
    def __getitem__(self, index):
        return 42

class ReturnYes(object):
    """ can't be properly infered """
    missing = Missing()

def log(message, message_type="error"):
    """ Test """
    return message

def print_good():
    """ Good format strings """
    print "{0} {1}".format(1, 2)
    print "{0!r:20}".format("Hello")
    print "{!r:20}".format("Hello")
    print "{a!r:20}".format(a="Hello")
    print "{pid}".format(pid=os.getpid())
    print str("{}").format(2)
    print "{0.missing.length}".format(ReturnYes())
    print "{1.missing.length}".format(ReturnYes())
    print "{a.ids[3][1]}".format(a=Test())
    print "{a[0][0]}".format(a=[[1]])
    print "{[0][0]}".format({0: {0: 1}})
    print "{a.test}".format(a=Custom())
    print "{a.__len__}".format(a=[])
    print "{a.ids.__len__}".format(a=Test())
    print "{a[0]}".format(a=Getitem())
    print "{a[0][0]}".format(a=[Getitem()])
    print "{[0][0]}".format(["test"])
    # these are skipped
    print "{0} {1}".format(*[1, 2])
    print "{a} {b}".format(**{'a': 1, 'b': 2})
    print "{a}".format(a=Missing())

def pprint_bad():
    """Test string format """
    print "{{}}".format(1)
    print "{} {".format()
    print "{} }".format()
    print "{0} {}".format(1, 2)
    print "{a} {b}".format(a=1, c=2)
    print "{} {a}".format(1, 2)
    print "{} {}".format(1)
    print "{} {}".format(1, 2, 3)
    print "{a} {b} {c}".format()
    print "{} {}".format(a=1, b=2)
    print "{a} {b}".format(1, 2)
    print "{0} {1} {a}".format(1, 2, 3)
    print "{a.ids.__len__.length}".format(a=Test())
    print "{a.ids[3][400]}".format(a=Test())
    print "{a.ids[3]['string']}".format(a=Test())
    print "{[0][1]}".format(["a"])
    print "{[0][0]}".format(((1, )))
    print "{b[0]}".format(a=23)
    print "{a[0]}".format(a=object)
    print log("{}".format(2, "info"))
    print "{0.missing}".format(2)

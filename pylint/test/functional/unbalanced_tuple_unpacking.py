"""Check possible unbalanced tuple unpacking """
from __future__ import absolute_import
from functional.unpacking import unpack

__revision__ = 0

def do_stuff():
    """This is not right."""
    first, second = 1, 2, 3 # [unbalanced-tuple-unpacking]
    return first + second

def do_stuff1():
    """This is not right."""
    first, second = [1, 2, 3] # [unbalanced-tuple-unpacking]
    return first + second

def do_stuff2():
    """This is not right."""
    (first, second) = 1, 2, 3 # [unbalanced-tuple-unpacking]
    return first + second

def do_stuff3():
    """This is not right."""
    first, second = range(100)
    return first + second

def do_stuff4():
    """ This is right """
    first, second = 1, 2
    return first + second

def do_stuff5():
    """ This is also right """
    first, second = (1, 2)
    return first + second

def do_stuff6():
    """ This is right """
    (first, second) = (1, 2)
    return first + second

def temp():
    """ This is not weird """
    if True:
        return [1, 2]
    return [2, 3, 4]

def do_stuff7():
    """ This is not right """
    first, second = temp() # [unbalanced-tuple-unpacking]
    return first + second

def temp2():
    """ This is weird, but correct """
    if True:
        return (1, 2)
    else:
        if True:
            return (2, 3)
    return (4, 5)

def do_stuff8():
    """ This is correct """
    first, second = temp2()
    return first + second

def do_stuff9():
    """ This is not correct """
    first, second = unpack() # [unbalanced-tuple-unpacking]
    return first + second

class UnbalancedUnpacking(object):
    """ Test unbalanced tuple unpacking in instance attributes. """
    # pylint: disable=attribute-defined-outside-init, invalid-name, too-few-public-methods
    def test(self):
        """ unpacking in instance attributes """
        self.a, self.b = temp() # [unbalanced-tuple-unpacking]
        self.a, self.b = temp2()
        self.a, self.b = unpack() # [unbalanced-tuple-unpacking]


def issue329(*args):
    """ Don't emit unbalanced tuple unpacking if the
    rhs of the assignment is a variable-length argument,
    because we don't know the actual length of the tuple.
    """
    first, second, third = args
    return first, second, third

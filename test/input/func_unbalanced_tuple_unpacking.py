"""Check possible unbalanced tuple unpacking """

from input.unpacking import unpack

__revision__ = 0

def do_stuff():
    """This is not right."""
    first, second = 1, 2, 3
    return first + second

def do_stuff1():
    """This is not right."""
    first, second = [1, 2, 3]
    return first + second

def do_stuff2():
    """This is not right."""
    (first, second) = 1, 2, 3
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
    first, second = temp()
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
    first, second = unpack()
    return first + second

class UnbalancedUnpacking(object):
    """ Test unbalanced tuple unpacking in instance attributes. """
    # pylint: disable=attribute-defined-outside-init, invalid-name, too-few-public-methods
    def test(self):
        """ unpacking in instance attributes """
        self.a, self.b = temp()
        self.a, self.b = temp2()
        self.a, self.b = unpack()

"""Check possible unbalanced tuple unpacking """

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



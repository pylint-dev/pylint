"""Check possible unbalanced tuple unpacking """

__revision__ = 0

def do_stuff():
    """This is not right."""
    first, second = 1, 2, 3
    return first + second

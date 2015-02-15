"""Check for duplicate function arguments."""
__revision__ = 1

def foo1(_, _):
    """Function with duplicate argument name."""
    pass

def foo2(_, *_):
    """Function with duplicate argument name."""
    pass

def foo3(_, _=3):
    """Function with duplicate argument name."""
    pass

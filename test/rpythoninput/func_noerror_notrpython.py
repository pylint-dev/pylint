def function(attrname):
    """NOT RPYTHON"""
    # I'm free ...
    yield getattr(unicode, attrname)
    yield getattr(str, attrname)
    
def entry_point(argv):
    return 0


def target(*args):
    return entry_point, None

def function(i):
    attr = None
    if i == 1:
        attr = 1
    else:
        attr = "hello"
    return attr

def entry_point(argv):
    function(len(argv))
    return 0


def target(*args):
    return entry_point, None

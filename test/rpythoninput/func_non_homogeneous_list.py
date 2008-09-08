GLOB = 1

def function(i):
    return [i, GLOB, "hop"]

def entry_point(argv):
    function(len(argv))
    return 0


def target(*args):
    return entry_point, None

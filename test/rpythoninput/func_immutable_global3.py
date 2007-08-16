
def function():
    from rpythoninput import immutable_global3
    immutable_global3.GLOB = 2 # was 1

def entry_point(argv):
    function()
    from rpythoninput import immutable_global3
    if immutable_global3.GLOB == 2:
        return 0
    return 1

def target(*args):
    return entry_point, None


GLOB = 1

def function():
    global GLOB
    GLOB = "value"

def entry_point(argv):
    function()
    if GLOB == 'value':
        return 0
    return 1

def target(*args):
    return entry_point, None


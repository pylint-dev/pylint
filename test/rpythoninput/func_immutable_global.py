GLOB = {}

def function():
    GLOB['key'] = "value"

def entry_point(argv):
    function()
    if GLOB['key'] == 'value':
        return 0
    return 1

def target(*args):
    return entry_point, None


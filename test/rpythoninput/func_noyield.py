import os

def function():
    yield "hello"
    yield "hello"
    yield "hello"
    
def entry_point(argv):
    count = 0
    for elt in function():
        count += 1
    if count == 3:
        return 0 # OK
    return 1 # ERROR

def target(*args):
    return entry_point, None

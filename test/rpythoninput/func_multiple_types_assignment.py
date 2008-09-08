import os

def function1(i):
    attr = None
    if i == 1:
        attr = 1
    else:
        attr = "hello"
    return attr

def function2(i):
    attr = None
    if i == 1:
        attr = 1
    return attr

def function_ok(i):
    attr = None
    if i == 1:
        attr = "hello"
    return attr

def entry_point(argv):
    os.write(str(function1(len(argv))))
    os.write(str(function_ok(len(argv))))
    return 0


def target(*args):
    return entry_point, None

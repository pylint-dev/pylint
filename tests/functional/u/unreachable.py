# pylint: disable=missing-docstring, broad-exception-raised

import signal
import sys

def func1():
    return 1
    print('unreachable') # [unreachable]

def func2():
    while 1:
        break
        print('unreachable') # [unreachable]

def func3():
    for i in (1, 2, 3):
        print(i)
        continue
        print('unreachable') # [unreachable]

def func4():
    raise Exception
    return 1 / 0 # [unreachable]


# https://github.com/PyCQA/pylint/issues/4698
def func5():
    """Empty generator functions should be allowed."""
    return
    yield

def func6():
    """Add 'unreachable' if yield is followed by another node."""
    return
    yield
    print("unreachable")  # [unreachable]

def func7():
    sys.exit(1)
    var = 2 + 2  # [unreachable]
    print(var)


class FalseExit:
    def exit(number):
        print(f"False positive this is not sys.exit({number})")

def func_false_exit():
    sys  = FalseExit()
    sys.exit(1)
    var = 2 + 2
    print(var)

def func8():
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    try:
        print(1)
    except KeyboardInterrupt:
        pass

#pylint: disable=missing-docstring, no-else-return
"""Testing inconsistent returns"""
import math

# These ones are consistent
def explicit_returns(var):
    if var >= 0:
        return math.sqrt(var)
    else:
        return None

def explicit_returns2(var):
    if var < 0:
        return None
    return math.sqrt(var)

def empty_implicit_returns(var):
    if var < 0:
        return

def returns_in_exceptions():
    try:
        raise ValueError('test')
    except ValueError:
        return 1
    except (OSError, TypeError):
        return 2

def returns_and_exceptions(var):
    if var < 10:
        return var**2
    else:
        raise ValueError("Incorrect value")

def explicit_returns3(arg):
    if arg:
        return False
    else:
        if arg < 3:
            print('arg < 3')
        return True

def nested_function():
    def dummy_return():
        return
    return dummy_return

# Next ones are not consistent
def explicit_implicit_returns(var): # [inconsistent-return-statements]
    if var >= 0:
        return math.sqrt(var)

def empty_explicit_returns(var): # [inconsistent-return-statements]
    if var < 0:
        return
    return math.sqrt(var)

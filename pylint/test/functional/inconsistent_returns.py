#pylint: disable=missing-docstring, no-else-return, invalid-name, unused-variable, superfluous-parens
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

def explicit_returns4(arg):
    if arg:
        if arg > 2:
            print('arg > 2')
        return False
    else:
        if arg < 3:
            print('arg < 3')
        return True

def explicit_returns5(arg):
    if arg:
        if arg > 2:
            print('arg > 2')
        return False
    else:
        return True

def nested_function():
    def dummy_return():
        return
    return dummy_return

def explicit_returns6(x, y, z):
    if x:  # pylint: disable=no-else-return
        a = 1
        if y:  # pylint: disable=no-else-return
            b = 2
            return y
        else:
            c = 3
            return x
    else:
        d = 4
        return z

def explicit_returns7(arg):
    if arg < 0:
        arg = 2 * arg
        return 'below 0'
    elif arg == 0:
        print("Null arg")
        return '0'
    else:
        arg = 3 * arg
        return 'above 0'

# Next ones are not consistent
def explicit_implicit_returns(var): # [inconsistent-return-statements]
    if var >= 0:
        return math.sqrt(var)

def empty_explicit_returns(var): # [inconsistent-return-statements]
    if var < 0:
        return
    return math.sqrt(var)

def explicit_implicit_returns2(arg): # [inconsistent-return-statements]
    if arg:
        if arg > 2:
            print('arg > 2')
            return False
    else:
        return True

def explicit_implicit_returns3(arg): # [inconsistent-return-statements]
    if arg:
        if arg > 2:
            print('arg > 2')
            return False
        else:
            return True

def returns_missing_in_catched_exceptions(arg): # [inconsistent-return-statements]
    try:
        arg = arg**2
        raise ValueError('test')
    except ValueError:
        print('ValueError')
        arg = 0
    except (OSError, TypeError):
        return 2

def complex_func(arg): # [inconsistent-return-statements]
    for i in range(arg):
        if i > arg / 2:
            break
        else:
            return arg

def inconsistent_returns_in_nested_function():
    def not_consistent_returns_inner(arg): # [inconsistent-return-statements]
        for i in range(arg):
            if i > arg / 2:
                break
            else:
                return arg
    return not_consistent_returns_inner

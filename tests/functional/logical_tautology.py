"""Check for logical tautology, when a value is compared against itself."""
# pylint: disable=missing-docstring, blacklisted-name, singleton-comparison, too-many-return-statements, inconsistent-return-statements, no-else-return, too-many-branches, bad-whitespace, literal-comparison

def foo():
    arg = 786
    if arg == arg: # [comparison-with-itself]
        return True
    elif arg != arg: # [comparison-with-itself]
        return True
    elif arg > arg: # [comparison-with-itself]
        return True
    elif arg <= arg: # [comparison-with-itself]
        return True
    elif None == None: # [comparison-with-itself]
        return None
    elif 786 == 786: # [comparison-with-itself]
        return True
    elif 786 is 786: # [comparison-with-itself]
        return True
    elif 786 is not 786: # [comparison-with-itself]
        return True
    elif arg is arg: # [comparison-with-itself]
        return True
    elif arg is not arg: # [comparison-with-itself]
        return True
    elif True is True: # [comparison-with-itself]
        return True
    elif 666 == 786:
        return False
    else:
        return None


def bar():
    arg = 666
    return 666 if arg != arg else 786 # [comparison-with-itself]

def foobar():
    arg = 786
    return arg > 786

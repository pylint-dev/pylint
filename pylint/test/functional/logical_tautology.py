"""Check for logical tautology, when a value is compared against itself."""
# pylint: disable=missing-docstring, blacklisted-name, singleton-comparison, too-many-return-statements, inconsistent-return-statements, no-else-return

def foo():
    arg = 786
    if arg == arg: # [logical-tautology]
        return True
    elif arg != arg: # [logical-tautology]
        return True
    elif arg > arg: # [logical-tautology]
        return True
    elif arg <= arg: # [logical-tautology]
        return True
    elif None == None: # [logical-tautology]
        return None
    elif 786 == 786: # [logical-tautology]
        return True
    elif 666 == 786:
        return False
    else:
        return None


def bar():
    arg = 666
    return 666 if arg != arg else 786 # [logical-tautology]

def foobar():
    arg = 786
    return arg > 786

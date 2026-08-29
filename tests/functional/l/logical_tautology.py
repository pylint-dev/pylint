"""Check for logical tautology, when a value is compared against itself."""
# pylint: disable=missing-docstring, disallowed-name, singleton-comparison, too-many-return-statements, inconsistent-return-statements, no-else-return, too-many-branches, literal-comparison

def foo(obj):
    arg = 786
    if arg == arg: # [comparison-with-itself]
        return True
    elif arg != arg: # [comparison-with-itself]
        return True
    elif obj.child.value != obj.child.value: # [comparison-with-itself]
        return True
    elif arg > arg: # [comparison-with-itself]
        return True
    elif arg.real > arg.real: # [comparison-with-itself]
        return True
    elif arg <= arg: # [comparison-with-itself]
        return True
    elif None == None:  # [comparison-of-constants, comparison-with-itself]
        return None
    elif 786 == 786:  # [comparison-of-constants, comparison-with-itself]
        return True
    elif 786 is 786:  # [comparison-of-constants, comparison-with-itself]
        return True
    elif 786 is not 786:  # [comparison-of-constants, comparison-with-itself]
        return True
    elif arg is arg: # [comparison-with-itself]
        return True
    elif arg is not arg: # [comparison-with-itself]
        return True
    elif True is True:  # [comparison-of-constants, comparison-with-itself]
        return True
    elif 666 == 786:  # [comparison-of-constants]
        return False
    else:
        return None


def bar():
    arg = 666
    return 666 if arg != arg else 786 # [comparison-with-itself]

def foobar():
    arg = 786
    return arg > 786


def compare_attributes(obj, other):
    return (
        obj.left == obj.right
        or obj.value == other.value
        or obj.factory().value == obj.factory().value
    )

"""docstring"""

__revision__ = ''

HEHE = {}

def function1(value=[]):
    """docstring"""
    print value

def function2(value=HEHE):
    """docstring"""
    print value

def function3(value):
    """docstring"""
    print value

def function4(value=set()):
    """set is mutable and dangerous."""
    print value

def function5(value=frozenset()):
    """frozenset is immutable and safe."""
    print value

GLOBAL_SET = set()

def function6(value=GLOBAL_SET):
    """set is mutable and dangerous."""
    print value

def function7(value=dict()):
    """dict is mutable and dangerous."""
    print value

def function8(value=list()):
    """list is mutable and dangerous."""
    print value

def function9(value=[1, 2, 3, 4]):
    """list with items should not output item values in error message"""
    print value

def function10(value={'a': 1, 'b': 2}):
    """dictionaries with items should not output item values in error message"""
    print value

def function11(value=list([1, 2, 3])):
    """list with items should not output item values in error message"""
    print value

def function12(value=dict([('a', 1), ('b', 2)])):
    """dictionaries with items should not output item values in error message"""
    print value

OINK = {
    'a': 1,
    'b': 2
}

def function13(value=OINK):
    """dictionaries with items should not output item values in error message"""
    print value

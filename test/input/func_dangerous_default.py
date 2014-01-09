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

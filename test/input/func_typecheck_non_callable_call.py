# pylint: disable=R0903
"""
    'E1102': ('%s is not callable',
              'Used when an object being called has been infered to a non \
              callable object'),
"""

__revision__ = None

__revision__()

def correct():
    """callable object"""
    return 1

__revision__ = correct()

class Correct(object):
    """callable object"""

class MetaCorrect(object):
    """callable object"""
    def __call__(self):
        return self
    
INSTANCE = Correct()
CALLABLE_INSTANCE = MetaCorrect()
CORRECT = CALLABLE_INSTANCE()
INCORRECT = INSTANCE()
LIST = []
INCORRECT = LIST()
DICT = {}
INCORRECT = DICT()
TUPLE = ()
INCORRECT = TUPLE()
INT = 1
INCORRECT = INT()
